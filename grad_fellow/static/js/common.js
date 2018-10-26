let gfCommon = {
    getNonEmptyInput: function (message, _default) {
        while (true) {
            let r = prompt(message, _default);
            if (r === null) {
                return null;
            }
            r = $.trim(r);
            if (r === '') {
                alert('Input should not be empty');
            } else {
                return r;
            }
        }
    },
    logout: function (url, storageKey) {
        localStorage.removeItem(storageKey);
        location.assign(url);
    }
};
