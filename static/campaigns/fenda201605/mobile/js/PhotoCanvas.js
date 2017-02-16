function PhotoCanvas(canvasId, width, height, loadingDivId, bgImage) {
    this.canvas = document.getElementById(canvasId);
    this.context = this.canvas.getContext("2d");
    this.canvas.width = width;
    this.canvas.height = height;
    this.image = null;
    this.orientation = 1;
    this.xDimension = 0;
    this.yDimension = 0;
    this.loadingObj = document.getElementById(loadingDivId);
    this.bgImage = bgImage || null;
    if (this.bgImage) {
        this.context.drawImage(this.bgImage,
            0, 0, this.bgImage.width, this.bgImage.height,
            0, 0, this.canvas.width, this.canvas.height
        );
    }
}
PhotoCanvas.prototype = {
    _render: function() {
        var drawHeight = this.canvas.width / this.image.width * this.image.height;
        var offsetY = (this.canvas.height - drawHeight) / 2;
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        if (this.bgImage) {
            this.context.drawImage(this.bgImage,
                0, 0, this.bgImage.width, this.bgImage.height,
                0, 0, this.canvas.width, this.canvas.height
            );
        }
        this.context.drawImage(this.image,
            0, 0, this.image.width, this.image.height,
            0, offsetY, this.canvas.width, drawHeight
        );
        this._closeLoading();
    },
    // 返回校正后的图片
    _loadingBeforeFix: function() {
        this.loadingObj.style.visibility = "visible";
    },
    _closeLoading: function() {
        this.loadingObj.style.visibility = "hidden";
    },
    _fixOrientation: function(image, afterFix) {
        var tempCanvas = document.createElement("canvas");
        var tempContext = tempCanvas.getContext("2d");
        var realWidth = image.width;
        var realHeight = image.height;
        var transX = 0;
        var transY = 0;
        if (this.orientation != 1) {
            transX = parseInt(image.naturalWidth / 2);
            transY = parseInt(image.naturalHeight / 2);
        }
        switch(this.orientation){
            case 8:
                // 90 rotate left     --需要90度向左旋转。。那么，这个 PixelYDimension就是宽度了，PixelXDimension就是高度了。
                realWidth = this.yDimension;
                realHeight = this.xDimension;
                tempCanvas.width = realWidth;
                tempCanvas.height = realHeight;
                tempContext.translate(parseInt(realWidth/2),parseInt(realHeight/2));
                tempContext.rotate(-0.5 * Math.PI);
                tempContext.drawImage(image,
                    0, 0, image.width, image.height,
                    0 - transX, 0 - transY, image.width, image.height);
                break;
            case 3:
                //180向左旋转
                realWidth = this.xDimension;
                realHeight = this.yDimension;
                tempCanvas.width = realWidth;
                tempCanvas.height = realHeight;
                tempContext.translate(parseInt(realWidth/2),parseInt(realHeight/2));
                tempContext.rotate(Math.PI);
                tempContext.drawImage(image,
                    0, 0, image.width, image.height,
                    0 - transX, 0 - transY, image.width, image.height);
                break;
            case 6:
                //90 rotate right 需要向右旋转90度，PixelYDimension就是宽度了，PixelXDimension就是高度了。
                realWidth = this.yDimension;
                realHeight = this.xDimension;
                tempCanvas.width = realWidth;
                tempCanvas.height = realHeight;
                tempContext.translate(parseInt(realWidth/2),parseInt(realHeight/2));
                tempContext.rotate(0.5 * Math.PI);
                tempContext.drawImage(image,
                    0, 0, image.width, image.height,
                    0 - transX, 0 - transY, image.width, image.height);
                break;
        }
        var resultImage = new Image();
        resultImage.onload = function() {
            afterFix(resultImage);
        };
        resultImage.src = tempCanvas.toDataURL("image/png");
    },
    _toDataURL: function(multiplier) {
        if (multiplier === 1) {
            return this.canvas.toDataURL("image/png");
        } else {
            var desWidth = this.canvas.width * multiplier;
            var desHeight = this.canvas.height * multiplier;
            var tempCanvas = document.createElement("canvas");
            tempCanvas.width = desWidth;
            tempCanvas.height = desHeight;
            var tempContext = tempCanvas.getContext("2d");
            tempContext.drawImage(this.canvas,
            0, 0, this.canvas.width, this.canvas.height,
            0, 0, desWidth, desHeight);
            return tempCanvas.toDataURL("image/png");
        }
    },
    loadFile: function(file) {
        var self = this;
        self._loadingBeforeFix();
        var tempImage = new Image();
        tempImage.onload = function() {
            EXIF.getData(tempImage, function() {
                EXIF.getAllTags(this);
                var orientation = EXIF.getTag(this, 'Orientation');
                console.log(orientation);
                if (orientation === 8 || orientation === 3 || orientation === 6) {
                    self.orientation = orientation;
                    self.xDimension = EXIF.getTag(this, 'PixelXDimension');
                    self.yDimension = EXIF.getTag(this, 'PixelYDimension');
                    self._fixOrientation(tempImage, function(image){
                        self.image = image;
                        self._render();
                    });
                } else {
                    self.orientation = 1;
                    self.image = tempImage;
                    self._render();
                }
            });
        };
        var fileReader = new FileReader();
        fileReader.onload = function() {
            tempImage.src = fileReader.result;
        };
        fileReader.readAsDataURL(file);
    },
    toImageFile: function(multiplier) {
        if (!multiplier) multiplier = 1;
        var dataURL = this._toDataURL(multiplier);
        var arr = dataURL.split(','), mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
        while(n--){
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], {type:mime});
    },
    toImageSrc: function(multiplier) {
        if (!multiplier) multiplier = 1;
        return this._toDataURL(multiplier);
    }
};
