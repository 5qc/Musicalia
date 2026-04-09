function loadGenres() {
    const genre_data = JSON.parse(document.querySelector('meta[name="json:data"]').getAttribute("value"))["claims"]["P136"]
    const genre_id = <HTMLSpanElement>document.getElementById("genres")

    for (let i = 0; i < genre_data.length; i++) {
        const genre = genre_data[i]
        const g_id = genre["mainsnak"]["datavalue"]["value"]["id"]
        $.ajax({
            url: `https://www.wikidata.org/wiki/Special:EntityData/${g_id}.json`,
            dataType: "json",
            success: (data) => {
                const genreEl = <HTMLAnchorElement>document.getElementById(`genre_${zeropad(i + 1)}`)

                genreEl.innerHTML += `${data["entities"][g_id]["labels"]["en"]["value"]}`
                genreEl.href = `/genre/${g_id}`

                if (i !== genre_data.length - 1) {
                    genreEl.insertAdjacentHTML("afterend", "&nbsp;&bull;&nbsp;")
                }
            }
        })
    }
}