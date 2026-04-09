function loadExternalLinks() {
    // get data stored in attribute
    const full_data = JSON.parse(document.querySelector('meta[name="json:data"]').getAttribute("value"))

    // define names and images for each property
    const link_data = {
        "P2205": ["Spotify", "https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg"],
        "P2281": ["Apple Music", "https://upload.wikimedia.org/wikipedia/commons/5/5f/Apple_Music_icon.svg"],
        "P2723": ["Deezer", "https://upload.wikimedia.org/wikipedia/commons/0/0e/Deezer_New_Icon.svg"],
        "P4577": ["Tidal", "https://upload.wikimedia.org/wikipedia/commons/4/41/Tidal_%28service%29_logo_only.svg"],
        "P1954": ["Discogs", "https://upload.wikimedia.org/wikipedia/commons/6/69/Discogs_record_icon.svg"],
        "P3192": ["last.fm", "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Last.fm_favicon.png/250px-Last.fm_favicon.png"],
        "P7067": ["Album of the Year", "https://upload.wikimedia.org/wikipedia/commons/1/14/Aoty2.png"],
        "P8392": ["Rate Your Music", "https://upload.wikimedia.org/wikipedia/commons/d/d0/Rate_Your_Music_logo.svg"],
        "P1729": ["AllMusic", "https://upload.wikimedia.org/wikipedia/commons/e/ef/AllMusic_favicon.svg"]
    }

    // get and display links
    for (let property of [...Object.keys(link_data)]) {
        const data = full_data["claims"][property]
        const link = <HTMLAnchorElement>document.getElementById(property)

        if (data) { // if property is in item
            const value = chooseOne(data)
            const repl: string = value["mainsnak"]["datavalue"]["value"]

            $.ajax({
                url: `https://www.wikidata.org/wiki/Special:EntityData/${property}.json`,
                dataType: "json",
                success: (pData) => {
                    const url: string = chooseOne(pData["entities"][property]["claims"]["P1630"])["mainsnak"]["datavalue"]["value"]
                    const full_url: string = url.replace("$1", repl)

                    link.href = full_url
                    link.target = "_blank"
                    link.title = link_data[property][0]
                    link.innerHTML = `<img src="${link_data[property][1]}" height="35" alt="${link_data[property][0]}" />`
                }
            })
        } else { // if property is not in item
            link.remove()
        }
    }
}