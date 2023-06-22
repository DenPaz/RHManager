const visibleProcessBar = (b) => {
    b ?
        document.querySelector('.process').classList.remove('d-none')
    :
        document.querySelector('.process').classList.add('d-none')
}

const changeProcessBarStatus = (s) => {
    const processBar = document.querySelector('.process-val')

    if (s <= 40)
        processBar.style.backgroundColor = 'red'
    else if (s <= 60)
        processBar.style.backgroundColor = 'orange'
    else if (s <= 80)
        processBar.style.backgroundColor = 'yellow'
    else if (s <= 100)
        processBar.style.backgroundColor = 'green'

    processBar.style.width = (s === 0 ? 10 : s) + '%'
}


const passReg = []
passReg.push(/(?=.*[A-Z].*[A-Z])/)
passReg.push(/(?=.*[!@#$&*])/)
passReg.push(/(?=.*[0-9].*[0-9])/)
passReg.push(/(?=.*[a-z].*[a-z].*[a-z])/)
passReg.push(/.{8}/)

window.onload = function () {
    document.getElementById('id_password1').onkeyup = (e) => {
        if (e.target.value.length !== 0)
            visibleProcessBar(true)
        else
            visibleProcessBar(false)

        let count = 0
        for (let i = 0; i < passReg.length; i++) {
            if (new RegExp(passReg[i]).test(e.target.value) )
                count += 1
        }

        changeProcessBarStatus(count * 100 / 5 )
    }
}