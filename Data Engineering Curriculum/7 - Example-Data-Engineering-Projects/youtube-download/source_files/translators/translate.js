// needs an expensive API key https://github.com/LibreTranslate/LibreTranslate

async function make_request() {
    let res = await fetch("https://libretranslate.com/translate", {
        method: "POST",
        body: JSON.stringify({
          q: "Ciao!",
          source: "auto",
          target: "en"
        }),
        headers: { "Content-Type": "application/json" }
      });

      console.log(await res.json());
}

// make_request();