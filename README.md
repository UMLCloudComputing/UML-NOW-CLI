# UML-NOW-CLI <img src= "https://github.com/UMLCloudComputing/UML-NOW-CLI/assets/136134023/1ee7860e-a24b-40e2-8486-447733bbbcf8" width="100" height="100">

A Command Line Interface for the University of Massachusetts Lowell's NOW Student Dashboard API. Currently a work in progress.

**By using this, you agree to the terms and conditions set forth in the [University of Massachusetts Lowell API Terms of Service](https://www.uml.edu/api/Static/tos.html).**

## Installation

Install with pip:

```
pip3 install git+https://github.com/UMLCloudComputing/UML-NOW-CLI --force-reinstall
```

If you get `error: externally-managed-environment`, then you need to create a virtual environment.

You can create a virtual environment through 
```
python3 -m venv /path/to/venv
```
You can activate a virtual environment through 
```
source /path/to/venv/bin/activate
```

If you would like to create a shortcut script, copy the `umlnow.sh` file into your user or system bin folder.

## Basic Usage

The following commands can be used to output data:

- Course
- Search (in progress)
- API

### Course

This command utilizes web-scraping to extract information about a specific course from the UML Course Catalog website without using the API. **Note that this may produce inaccurate results if there is an error parsing the data.**

The `course` command expects a **course prefix** combined with a **course number**. Examples:

- `COMP.1010`
- `EECE.2020`
- `MATH.2310`

```
python3 -m umlnow course COMP.1020
```

```
{
    "name": "COMP.1020 Computing II (Formerly 91.102)",
    "url": "https://www.uml.edu/catalog/courses/COMP/1020/",
    "id": "008056",
    "description": "Computing II focuses on the implementation and applications of data structures, including arrays, linked lists, stacks, queues, trees, binary trees, binary search trees, heaps, graphs, and hash tables. Recursive approaches are used. Performance analysis is discussed. Attention is paid to programming style, documentation, and testing. This course includes extensive laboratory work. Effective Fall 2013, Co-req: Computing 2 Lab.",
    "credits": {
        "min": "3",
        "max": "3"
    },
    "requirements-text": "COMP.1010 Computing I with a B- or better, and COMP.1030L Computing I Lab, and Co-req: COMP.1040L Computing II Lab.",
    "requirements": {
        "prerequisites": [
            [
                "COMP.1010"
            ],
            [
                "COMP.1030L"
            ]
        ],
        "corequisites": [
            [
                "COMP.1040L"
            ]
        ]
    }
}
```

It also allows getting specific data:

```
$ python3 -m umlnow course COMP.1010 --requirements
```

```
{
    "requirements": {
        "prerequisites": [
            [
                "COMP.1010"
            ],
            [
                "COMP.1030L"
            ]
        ],
        "corequisites": [
            [
                "COMP.1040L"
            ]
        ]
    }

```

The parser will automatically try to extract the requirements string into structured class requirements. Both `prerequisites` and `corequisites` are lists of requirements. Each requirement is a list too. If there are multiple optional requirements, then there will be a list of optional classes in each requirement. Otherwise, there will just be one class in each requirement.

#### Course: History

The `--history` flag uses the `api` command under the hood to get a history of when the course was taught. This history goes back to Fall 2015.

```
python3 -m umlnow course COMP.5450 --history
```

To filter results by professor or semester or both, you can use the `--prof` and `--semester` flags.

```
python3 -m umlnow course COMP.1010 --history --prof david,adams
```

```
python3 -m umlnow course COMP.1010 --history --semester fall 
```

```
python3 -m umlnow course COMP.1010 --history --semester fall --prof david,adams
```


### Search

An abstraction layer that combines features of the UML Now API and the UML Course Catalog API.

Sub commands:

- courses
- professors
- programs
  - majors
  - minors
- pathways

#### Search: Courses

Provides the ability to query for all courses offered by UML.

To see all courses offered by UML:

```bash
python3 -m umlnow search courses
```

To see all courses offered by a department prefix

```bash
python3 -m umlnow search courses --departments=COMP
```

##### Using the `--parse` flag

By default, the search command just scrapes and returns results from the UML Course Catalog search page: https://www.uml.edu/catalog/advance-search.aspx.

The data provided is only the course prefix, name, and id. If you want to get all the details from a course like from the `umlnow course` command, you can do so by including the `--parse` flag.

**However, this requests a new webpage from the UML website for every course found. Using this flag on a large queryset (like all the courses) will take a long time to run and could break the terms of the UML website. Use this flag at your own risk.**

#### Search: Professors

***Not Implmented***

Provides the ability to query for all professors teaching courses at UML.

#### Search: Programs

***Not Implmented***

Provides the ability to query for all programs offered at UML.

#### Search: Pathways

***Not Implmented***

Provides the ability to query for degree-pathways offered by UML.

### API

***Needs Documentation***

If you want to access the UML APIs directly, use the following commands. This is useful for testing or exploring what the APIs can provide.

#### API: Search

Query the UML Now API directly.

```
python3 -m umlnow api search --term=3210 --subjects=COMP
```

```
python3 -m umlnow api search --term=3210 --subjects=COMP --courseTitle=computing
```

#### API: Catalog

Query the UML Catalog API directly.

```
python3 -m umlnow api catalog --pathCollege=SCI --pathDepartment=LCOMPSCI --pathType=undergraduate --SearchType=path
```

## Library

To use within your own Python program as a library, simply import the commands.

```python
from umlnow import course, Search, API
```

### Course API

Import the Course API with

```python
from umlnow import course
```

Function signature:
```
def Course(course, **kwargs):
```
Where course is the course ID as a string `"COMP.1020"` and kwargs are the information you want to retrieve. The following pieces of information are supported
- `name` - The name of the course
- `url` - The UML NOW page for the course
- `id` - ID of the course
- `description` - A description of the course 
- `credits` - The number of credits of the course
- `requirements-text`
- `requirements` - Parsed Course Requirements

If you specify no kwargs, all pieces of information will be returned as a dictionary in this format

```yaml
{
    'name': course_name,
    'url': course_url,
    'id': course_id,
    'description': course_description,
    'credits': course_credits,
    'requirements-text': requirements_text,
    'requirements': parsed_requirements,
}
```

Otherwise, only the specified entries will be returned. You can specify specific entries by setting the kwarg value to true. For example, if you wanted to just get the name and the description, you would use
`Course("COMP.1020", name=True, description=True)`

And this would be returned.
```yaml
{
    'name': course_name,
    'description': course_description,
}
```
