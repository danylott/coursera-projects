/**
 * @param {Number} hours
 * @param {Number} minutes
 * @param {Number} interval
 * @returns {String}
 */
module.exports = function (hours, minutes, interval) {
    let res_hours = Math.floor((hours + (minutes + interval) / 60) % 24);
    let res_minutes = Math.floor((minutes + interval) % 60);
    if(res_hours < 10) {
        res_hours = `0${res_hours}`;
    } else {
        res_hours = `${res_hours}`;
    }
    if(res_minutes < 10) {
        res_minutes = `0${res_minutes}`;
    } else {
        res_minutes = `${res_minutes}`;
    }
    return res_hours + ":" + res_minutes;
};
