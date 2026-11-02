// CV layout. Data comes from cv.json, which scripts/build_cv.py generates
// from _data/cv.yml, _data/service.yml, _publications/ and _talks/.
#let data = json("cv.json")

#set document(title: data.name + " - CV", author: data.name)
#set page(
  paper: "a4",
  margin: (x: 1.9cm, top: 1.6cm, bottom: 1.8cm),
  footer: context {
    set text(8pt, fill: luma(110))
    data.name
    h(1fr)
    counter(page).display() + " / " + str(counter(page).final().first())
  },
)
#set text(font: "Libertinus Serif", size: 10pt)
#set par(leading: 0.55em, spacing: 0.7em)
#show link: set text(fill: rgb("#1a4f8b"))
#set list(indent: 0.4em, body-indent: 0.5em, spacing: 0.45em)

#let section(title) = {
  v(0.8em)
  text(size: 11.5pt, weight: "bold", tracking: 0.04em, upper(title))
  v(-0.55em)
  line(length: 100%, stroke: 0.5pt + luma(120))
  v(0.1em)
}

#let org-link(e) = if "url" in e { link(e.url)[#e.org] } else { e.org }

#let entry(e) = block(breakable: false, below: 0.9em)[
  #grid(
    columns: (1fr, auto),
    [*#e.title*, #org-link(e)],
    text(fill: luma(60))[#e.start -- #e.end],
  )
  #if e.location != "" [
    #text(style: "italic", fill: luma(90))[#e.location]
  ]
  #if "bullets" in e and e.bullets.len() > 0 {
    v(-0.3em)
    for b in e.bullets [
      - #b
    ]
  }
]

#let mark-name(s) = s.split(data.name).join(strong(data.name))

// Header
#align(center)[
  #text(23pt, weight: "bold")[#data.name]
  #v(0.1em)
  #{
    let items = (
      data.location,
      link("mailto:" + data.email)[#data.email],
      link(data.website)[#data.website.replace("https://", "")],
    )
    items.join("  |  ")
  }
  #linebreak()
  #{
    let items = (
      link("https://orcid.org/" + data.orcid)[ORCID #data.orcid],
      link(data.scholar)[Google Scholar],
      link(data.github)[GitHub],
      link(data.linkedin)[LinkedIn],
    )
    items.join("  |  ")
  }
]

#v(0.3em)
*Languages:* #data.languages

#section("Professional Experience")
#for e in data.experience { entry(e) }

#section("Education")
#for e in data.education { entry(e) }

#section("Awards")
#for a in data.awards [
  - #a
]

#section("Publications")
#for p in data.publications {
  block(breakable: false, below: 0.6em)[
    #mark-name(p.authors)#if p.authors != "" [. ]#emph(p.title). #p.venue, #p.year.#if p.note != "" [ #p.note]
  ]
}

#section("Talks")
#for t in data.talks [
  - #strong(t.title), #t.venue#if t.location != "" [, #t.location], #t.date.
]

#section("Teaching and Supervision")
#set text(size: 9.5pt)
*Supervision at Paderborn University*
#for a in data.supervision [
  - #a
]
#v(0.3em)
*Teaching assistance*
#for a in data.teaching_assistance [
  - #a
]
#set text(size: 10pt)

#section("Service")
#for s in data.service {
  block(below: 0.6em)[*#s.title.* #s.items.join("; ").]
}
