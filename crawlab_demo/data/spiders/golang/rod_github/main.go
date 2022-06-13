package main

import (
	sdk "github.com/crawlab-team/crawlab-sdk"
	"github.com/crawlab-team/crawlab-sdk/entity"
	"github.com/go-rod/rod"
)

func main() {
	page := rod.New().MustConnect().MustPage("https://github.com/trending")
	page.MustWaitLoad()
	els := page.MustElements("article.Box-row")
	for _, el := range els {
		var desc string
		elDesc, err := el.Element("p")
		if err == nil {
			desc = elDesc.MustText()
		}
		var lang string
		elLang, err := el.Element("span[itemprop=\"programmingLanguage\"]")
		if err == nil {
			lang = elLang.MustText()
		}
		item := entity.Result{
			"name":        el.MustElement(".h3.lh-condensed > a").MustText(),
			"url":         el.MustElement(".h3.lh-condensed > a").MustAttribute("href"),
			"description": desc,
			"lang":        lang,
		}
		sdk.SaveItem(item)
	}
}
