/**
 * @param {String} tweet
 * @returns {String[]}
 */
module.exports = function (tweet) {
    words = tweet.split(' ');
    return words.reduce((hash_tags, word) => {
        if(word.startsWith('#')) {
            hash_tags.push(word.slice(1, word.length));
        }
        return hash_tags;
    }, []);
};
