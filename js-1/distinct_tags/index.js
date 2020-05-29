/**
 * @param {String[]} hashtags
 * @returns {String}
 */
module.exports = function (hashtags) {
    return hashtags.reduce((distinct_hashtags_list, hashtag) => {
        if(distinct_hashtags_list.indexOf(hashtag.toLowerCase()) === -1) {
            distinct_hashtags_list.push(hashtag.toLowerCase());
        }
        return distinct_hashtags_list;
    }, []).join(', ');
};
