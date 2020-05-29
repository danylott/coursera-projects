// Телефонная книга
var phoneBook = {};

/**
 * @param {String} command
 * @returns {*} - результат зависит от команды
 */
module.exports = function (command) {
    'use strict'

    let request = command.split(' ');
    
    let task = request[0];
    let phone;
    switch(task) {
        case 'ADD':
            let name = request[1];
            phone = request[2];
            let phones;
            if(phone.indexOf(',') > 0) {
                phones = request[2].split(',');
            } else {
                phones = [phone];
            }
            if(phoneBook.hasOwnProperty(name)) {
                phoneBook[name] = phoneBook[name].concat(phones);
            } else {
                phoneBook[name] = phones;
            }
            return true;
            break;
        case 'REMOVE_PHONE':
            let finded = false;
            phone = request[1];
            Object.keys(phoneBook).map((key, index) => {
                phoneBook[key].forEach((value, index, array) => {
                    if(value == phone) {
                        phoneBook[key].splice(index, 1);
                        finded = true;
                    }
                })
            });
            return finded;
        case 'SHOW':
            let result = [];
            Object.keys(phoneBook).forEach((value, index, array) => {
                if(phoneBook[value].length > 0)
                    result.unshift(value + ': ' + phoneBook[value].join(', '))
            })
            return result;
    }
};
