#!/usr/bin/env bash

mkdir -p data
echo '[]' > data/items.json
echo '[]' > data/tags.json
cat > data/skills.json <<- EOM
{
  "titles": [
    "Skills"
  ],
  "data": [
    [
      {
        "axis": "Software Engineering",
        "value": 0.1
      },
      {
        "axis": "Neuroscience",
        "value": 0.2
      },
      {
        "axis": "Psychology",
        "value": 0.3
      },
      {
        "axis": "Philosophy",
        "value": 0.4
      },
      {
        "axis": "Theology",
        "value": 0.5
      },
      {
        "axis": "Art",
        "value": 0.6
      },
      {
        "axis": "History",
        "value": 0.7
      },
      {
        "axis": "Geography",
        "value": 0.8
      },
      {
        "axis": "Biology",
        "value": 0.9
      },
      {
        "axis": "Chemistry",
        "value": 1.0
      },
      {
        "axis": "Geology",
        "value": 0.9
      },
      {
        "axis": "Astronomy",
        "value": 0.8
      },
      {
        "axis": "Astrophysics",
        "value": 0.7
      },
      {
        "axis": "Physics",
        "value": 0.6
      },
      {
        "axis": "Maths",
        "value": 0.5
      }
    ]
  ]
}
EOM