function chooseOne(list: any[]) {
    let l = []

    for (let i = 0; i < list.length; i++) {
        const x = list[i]
        if (x["rank"] === "deprecated") continue
        if (x["rank"] === "preferred") l = []

        l.push(x)

        if (x["rank"] === "preferred") break
    }

    return l[0]
}