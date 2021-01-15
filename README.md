# CERN-www-fonts

[![The Rebuild of the World Wide Web](https://worldwideweb.cern.ch/images/www_project.png)](https://worldwideweb.cern.ch)

## Project info

In February 2019, in celebration of the thirtieth anniversary of the World Wide Web, a team of developers and designers met at [CERN](https://www.cern.ch) to rebuild the original WorldWideWeb browser within a contemporary browser. 

The original WorldWideWeb browser was developed in 1990 on a [NeXT machine](https://en.wikipedia.org/wiki/NeXT_Computer), and recreating the entirely text-based experience would require the “jaggies” of the bitmap fonts used by the [NeXTSTEP operating system](https://en.wikipedia.org/wiki/NeXTSTEP). Attempts to change the rendering settings of contemporary fonts did not get close enough to the look and feel of the original, so the team created the **CERN-www** family of pixel fonts, meticulously vectorizing each pixel by hand to simulate the typography of the original WorldWideWeb.

The original sans serif fonts on the NeXT were versions of [Helvetica](https://fontsinuse.com/typefaces/44/helvetica), and the monospace was Ohlfs, designed by Keith Ohlfs.

Team members [Mark Boulton](http://markboulton.co.uk) and [Brian Suda](https://suda.co.uk) spearheaded the creation of the CERN-www fonts, and [David Jonathan Ross](https://djr.com) provided remote assistance with font development. 

As team member [Remy Sharp said](https://remysharp.com/2019/02/15/cern-day-4#it-looks-awfulwhich-is-great) about the project, “it looks awful...which is great!”


## Links

* [More about the project and team](https://worldwideweb.cern.ch)
* [More about the fonts](https://worldwideweb.cern.ch/typography/)
* [The WorldWideWeb browser rebuild](https://worldwideweb.cern.ch/browser/)

## Building the fonts

To build TTF, WOFF, and WOFF2 binaries from the [UFO](http://unifiedfontobject.org) sources, run [`souces/build.py`](https://github.com/djrrb/CERN-www-fonts/blob/master/sources/build.py) (requires [fontmake](https://github.com/googlei18n/fontmake)):
```
$ cd sources
$ python3 build.py
```

*Note: To make the numbers add up a little nicer, not all fonts use 1000 units per em.*

## Using the fonts

To match the font sizes in the [browser rebuild](https://worldwideweb.cern.ch/browser/), use the following pixel sizes:

* Headline: 20px
* 14: 14px
* Text: 13px (line-height: 14px)
* Mono: 10px

This is the CSS that was used to remove font-smoothing in certain browsers/OS combinations:

```
font-smooth: none;
font-smooth: never;
-webkit-font-smoothing: none;
-moz-font-smoothing: none;
```

See [`fonts/index.html`](https://github.com/djrrb/CERN-www-fonts/blob/master/fonts/index.html) for a sample implementation.

## Repository layout

This font repository structure is inspired by [Unified Font Repository v0.3](https://github.com/unified-font-repository/Unified-Font-Repository).

