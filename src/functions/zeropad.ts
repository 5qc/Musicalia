function zeropad(num: any) { // @ts-ignore
    if (typeof num !== Number) {
        num = Number(num)
    }

    if (num < 10) return `0${num}`
    else return `${num}`
}