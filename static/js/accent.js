let gameIndex = 0
let vowels = 'аоэеиыуёюя'
let truth = 0
let untruth = 0
let mistakes = []

function setWord(word) {
    let formattedWord = ''
    let hasTip = (word[0] === '(')
    for (let i = 0; i < word.length; i++) {
        if (word[i] === ')') {
            hasTip = false
        }
        if (hasTip === false) {

            if (vowels.indexOf(word[i].toLowerCase()) !== -1) {
                formattedWord = formattedWord + '<span onclick="addNum(this)" class="vowel letter">' + word[i] + '</span>'
            } else {
                formattedWord = formattedWord + '<span class="consonant letter">' + word[i] + '</span>'
            }
        } else {
            formattedWord = formattedWord + '<span class="letter">' + word[i] + '</span>'
        }
    }
    document.getElementById("word").innerHTML = formattedWord
}

function addNum(el) {
    if (el.textContent === el.textContent.toUpperCase()) {
        truth++
    } else {
        untruth++
        document.querySelector('#attention-info ul').appendChild(document.createElement('li')).innerHTML = words[gameIndex]
    }

    setTimeout(() => {
        if (gameIndex === words.length - 1) {
            document.getElementById('attention-info').style.display = 'block'
            document.getElementById('game').style.display = 'none'

        } else {
            gameIndex++
            setWord(words[gameIndex])
            document.getElementById("lap").innerHTML = (gameIndex + 1) + '/' + words.length
            document.getElementById("truth").innerHTML = truth
            document.getElementById("untruth").innerHTML = untruth

        }
    }, 100)

}