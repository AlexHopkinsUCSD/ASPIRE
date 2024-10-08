# API

| URL | Method | Router .py file | input/output link | Description |
| --- | ------ | --------------- | ----------------- | ----------- |
| /register | POST | test | [Input](#register-inputs)-[Output](#register-outputs)| Adds an entry to the "course" table, creates a new domain entry using supplied course content if no pre-existing domain is selected. |
| /module | POST | test | [Input](#module-inputs)-[Output](#module-outputs) | Uses supplied module contents to identify concepts taught in a module and the prerequisite concepts required to learn the module concepts. Adds a new module, and all new concepts/concept relationships to the database |
| /quiz/'id:int'/'type:str' | GET | test | [Input](#quizidtype-inputs)-[Output](#quizidtype-outputs) | Generates 20 multiple choice questions with answer feedback from the concepts specified by the module id and quiz type provided |
| /quiz | POST | test | [Input](#quiz-inputs)-[Output](#quiz-outputs) | Takes 5 MCQ questions with feedback, saves the questions to the database with a relationship to their associated concepts, creates and returns a Canvas-compatible .zip file |
| /module/join | POST | test | [Input](#modulejoin-inputs)-[Output](#modulejoin-outputs) | Adds an existing module to a course |
| /domain | PUT | test | test | Accepts a list of instruction sets, modifies the domain structure (concepts, concept_to_concept, concept_to_module, concept_to_domain) accordingly. | 

# Input/Output Data Structure
All data structures are preliminary and not necessarily comprehensive, this is a just an early reference until we have the autogenerated API documentation. Feel free to make changes/additions as necessary.
## /register Inputs
 <table>
<tr>
<th>Condition</th>
<th>Input</th>
</tr>
<tr>
<td>SME wants to register a course with an existing domain</td>
<td>

```json
multipart/form-data:

Content-Type: multipart/form-data; boundary=-------<replace>

---------<replace>
Content-Disposition: form-data; name="domain_id"

integer: domain ID
---------<replace>
Content-Disposition: form-data; name="name"

string: name of course
---------<replace>
Content-Disposition: form-data; name="quarter"

date: quarter start date
---------<replace>
Content-Disposition: form-data; name="professor"

string: name of professor
---------<replace>
Content-Disposition: form-data; name="courseContentTest"

<Text of supplied course content, might need to compress this as .GZIP file or find some other option for large amounts of text>
---------<replace>
Content-Disposition: form-data; name="courseContentImage-1" filename="image.pdf"

<binary data of image.pdf>
---------<replace>

```

</td>
</tr>
<tr>
<td>SME wants to register their course to a new domain (no domain_id supplied)</td>
<td>

```json
multipart/form-data:

Content-Type: multipart/form-data; boundary=-------<replace>

---------<replace>
Content-Disposition: form-data; name="name"

string: name of course
---------<replace>
Content-Disposition: form-data; name="quarter"

date: quarter start date
---------<replace>
Content-Disposition: form-data; name="professor"

string: name of professor
---------<replace>
Content-Disposition: form-data; name="courseContentText"

<Text of supplied course content, might need to compress this as .GZIP file or find some other option for large amounts of text>
---------<replace>
Content-Disposition: form-data; name="courseContentImage-1" filename="image.pdf"

<binary data of image.pdf>
---------<replace>

```

</td>
</tr>
</table>

## /register Outputs

 <table>
<tr>
<th>Condition</th>
<th>Status</th>
<th>Output</th>
</tr>
<tr>
<td>System successfully generates new course with pre-existing domain</td>
<td>200</td>
<td>

```json
{
    "course_id": int,
    "domain_id": int
}

```

</td>
</tr>
<tr>
<td><b>Invalid Domain:</b> domain does not exist</td>
<td>404</td>
<td>

```json

{
    "message": "Domain does not exist at id: <insert domain_id>"
}

```

</td>
</tr>
</tr>
<tr>
<td>System successfully creates new course and domain</td>
<td>200</td>
<td>

```json

{
    "course_id": int,
    "domain_id": int
}

```

</td>
</tr>
<tr>
<td>Invalid course content</td>
<td>400</td>
<td>

```json

{
    "invalid_file_names": [str]
}

```

</td>
</tr>
</table>

## /module Inputs

<table>
<tr>
<th>Condition</th>
<th>Input</th>
</tr>
<tr>
<td>SME wants to add a new module to their course and domain</td>
<td>

```json
multipart/form-data:

Content-Type: multipart/form-data; boundary=-------<replace>

---------<replace>
Content-Disposition: form-data; name="course_id"

integer: course_id
---------<replace>
Content-Disposition: form-data; name="title"

string: name of module
---------<replace>
Content-Disposition: form-data; name="moduleContentText"

<Text of supplied module content, might need to compress this as .GZIP file or find some other option for large amounts of text>
---------<replace>
Content-Disposition: form-data; name="moduleContentImage-1" filename="image.pdf"

<binary data of image.pdf>
---------<replace>

```

</td>
</tr>
</table>

## /module Outputs

 <table>
<tr>
<th>Condition</th>
<th>Status</th>
<th>Output</th>
</tr>
<tr>
<td>System successfully creates a new module</td>
<td>200</td>
<td>

```json
{
    "module_id": int,
}

```

</td>
</tr>
<tr>
<td><b>Invalid course:</b> course does not exist</td>
<td>404</td>
<td>

```json
{
    "message": "Course does not exist at id: <insert course_id>"
}
```

</td>
</tr>
<tr>
<td><b>Invalid course:</b> user does not have access to the course</td>
<td>403</td>
<td>

```json
{
    "message": "user does not have access to course at id: <insert course_id>"
}
```

</td>
</tr>
<tr>
<td>Invalid module content</td>
<td>400</td>
<td>

```json
{
    "invalid_file_names": [str]
}
```

</td>
</tr>
</table>

## /quiz/id/type Inputs

<table>
<tr>
<th>Condition</th>
<th>Input</th>
</tr>
<tr>
<td>SME wants to generate 20 MCQs</td>
<td>

```json
URL Params

module_id: int
quiz_type: str("preview", "review", "prereq")

```

</td>
</tr>
</table>

## /quiz/id/type Outputs

 <table>
<tr>
<th>Condition</th>
<th>Status</th>
<th>Output</th>
</tr>
<tr>
<td>System successfully creates a 20 MCQs</td>
<td>200</td>
<td>

```json
{
    "questions": [
        {
            "question": str,
            "concept_id": int,
            1: str/int,
            "feedback_1": str,
            ...
            4: str/int,
            "feedback_4": str,
            "correct_answer": int 
        },
        {...}
    ]
}

```

</td>
</tr>
<tr>
<td><b>Invalid parameters:</b> invalid type</td>
<td>404</td>
<td>

```json
{
    "message": "Expected: ('preview', 'review', or 'prereq') Received: <insert type>"
}
```

</td>
</tr>
<tr>
<td><b>Invalid parameters:</b> module does not exist</td>
<td>404</td>
<td>

```json
{
    "message": "Module does not exist at id: <insert id>"
}
```

</td>
</tr>
</table>

## /quiz Inputs

<table>
<tr>
<th>Condition</th>
<th>Input</th>
</tr>
<tr>
<td>SME wants to generate an MCQ quiz .zip file</td>
<td>

```json
{
    "questions": [
        {
            "question": str,
            "concept_id": int,
            1: str/int,
            "feedback_1": str,
            ...
            4: str/int,
            "feedback_4": str,
            "correct_answer": int 
        },
        {...}
    ]
}
```

</td>
</tr>
</table>

## /quiz Outputs
 <table>
<tr>
<th>Condition</th>
<th>Status</th>
<th>Output</th>
</tr>
<tr>
<td>System successfully creates a quiz</td>
<td>200</td>
<td>

```json
Canvas-compliant .zip file

```

</td>
</tr>
<tr>
<td><b>Invalid question(s):</b> SME does not supply 5 questions</td>
<td>400</td>
<td>

```json
{
    "message": "invalid question quantity, expected 5 got <insert quantity>"
}
```

</td>
</tr>
<tr>
<td><b>Invalid question(s):</b> SME does not supply questions in proper format</td>
<td>400</td>
<td>

```json
{
    "message": "invalid question format"
}
```

</td>
</tr>
<tr>
<td><b>Invalid question(s):</b> concept_id attached to quiz question does not exist</td>
<td>404</td>
<td>

```json
{
    "message": "concept at ID <insert id> does not exist"
}
```

</td>
</tr>
</tr>
<tr>
<td>Failed to zip</td>
<td>400</td>
<td>

```json
{
    "message": "unable to return .zip file"
}
```

</td>
</tr>
</table>

## /module/join Inputs

<table>
<tr>
<th>Condition</th>
<th>Input</th>
</tr>
<tr>
<td>SME wants to reuse an existing module in their course</td>
<td>

```json
{
    "module_id": int,
    "course_id": int
}
```

</td>
</tr>
</table>

## /module/join Outputs
 <table>
<tr>
<th>Condition</th>
<th>Status</th>
<th>Output</th>
</tr>
<tr>
<td>System successfully joins module to course</td>
<td>200</td>
<td>

```json
{
    "message": "module successfully added to course"
}

```

</td>
</tr>
<tr>
<td><b>Invalid module_id:</b> module does not exist</td>
<td>404</td>
<td>

```json
{
    "message": "module does not exist at id: <insert id>"
}
```

</td>
</tr>
<tr>
<td><b>Invalid module_id:</b> module exists but is not part of the course domain</td>
<td>400</td>
<td>

```json
{
    "message": "module at id: <insert module_id> does not exist at domain: <insert domain_id>"
}
```

</td>
</tr>
</tr>
<tr>
<td><b>Invalid course_id:</b> Course does not exist</td>
<td>404</td>
<td>

```json
{
    "message": "course does not exist at id: <insert course_id>"
}
```

</td>
</tr>
<tr>
<td><b>Invalid course_id:</b> User does not have access to the selected course</td>
<td>403</td>
<td>

```json
{
    "message": "user does not have access to course at id: <insert course_id>"
}
```

</td>
</tr>
</table>