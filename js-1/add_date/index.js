/**
 * @param {String} date
 * @returns {Object}
 */
module.exports = function (date) {
    var date = new Date(+date.slice(0,4), +date.slice(5,7) - 1, +date.slice(8,10), +date.slice(11,13), +date.slice(14,16));
    return {
        value: date,
        setValue: function() {
            this.value = date.getFullYear() + '-' + this.addLeadingZero(Number(date.getMonth() + 1)) + '-' + this.addLeadingZero(date.getDate()) + ' ' + this.addLeadingZero(date.getHours()) + ':' + this.addLeadingZero(date.getMinutes())
        },
        addLeadingZero: function(value) {
            if(value < 10) {
                return '0' + value;
            }
            return String(value);
        },
        checkException: function(amount, type) {
            if(amount < 0 || !(['years', 'months', 'days', 'hours', 'minutes'].includes(type)))
                throw new TypeError;
        },
        add: function(amount, type){    
            this.checkException(amount, type);
            switch(type) {
                case 'years':
                    date.setFullYear(date.getFullYear() + amount);
                    break;

                case 'months':
                    date.setMonth(date.getMonth() + amount);
                    break;

                case 'days':
                    date.setDate(date.getDate() + amount);
                    break;

                case 'hours':
                    date.setHours(date.getHours() + amount);
                    break;

                case 'minutes':
                    date.setMinutes(date.getMinutes() + amount);
                    break;

            }
            this.setValue();
            return this;
        },
        subtract: function(amount, type){
            this.checkException(amount, type);
            switch(type) {
                case 'years':
                    date.setFullYear(date.getFullYear() - amount);
                    break;

                case 'months':
                    date.setMonth(date.getMonth() - amount);
                    break;

                case 'days':
                    date.setDate(date.getDate() - amount);
                    break;

                case 'hours':
                    date.setHours(date.getHours() - amount);
                    break;

                case 'minutes':
                    date.setMinutes(date.getMinutes() - amount);
                    break;
            }
            this.setValue();
            return this;
        }
    }
};
