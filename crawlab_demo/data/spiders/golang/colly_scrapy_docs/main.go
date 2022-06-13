package main

import (
	"fmt"
	sdk "github.com/crawlab-team/crawlab-sdk"
	"github.com/crawlab-team/crawlab-sdk/entity"
	"github.com/crawlab-team/go-trace"
	"github.com/gocolly/colly/v2"
)

func main() {
	c := colly.NewCollector()

	// save items
	c.OnHTML(".document", func(e *colly.HTMLElement) {
		item := entity.Result{
			"title":   e.ChildText("h1"),
			"url":     e.Request.URL.String(),
			"content": e.ChildText("div[itemprop=\"articleBody\"]"),
		}
		sdk.SaveItem(item)
	})

	// next page
	c.OnHTML("a[rel=\"next\"][href]", func(e *colly.HTMLElement) {
		url := e.Attr("href")
		if err := e.Request.Visit(url); err != nil {
			trace.PrintError(err)
		}
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL)
	})

	if err := c.Visit("https://docs.scrapy.org/en/latest/"); err != nil {
		trace.PrintError(err)
	}
}
