###### **JSON form used in the rss_reader utility**

`{
    "title": "News item title",
    "pubDate": "News publishing date",
    "link": "News item URL",
    "description": 
        {
            "text": "News item text",
            "links": "News item additional URLs",
            "images": "News item images URLs",
        },
}`


# News item

- [1. [Optional] Property `News item > title`](#title)
- [2. [Optional] Property `News item > pubDate`](#pubDate)
- [3. [Optional] Property `News item > link`](#link)
- [4. [Optional] Property `News item > description`](#description)
  - [4.1. Property `News item > description > text`](#description_text)
  - [4.2. Property `News item > description > links`](#description_links)
  - [4.3. Property `News item > description > images`](#description_images)

**Title:** News item

| Type                      | `object`                                                                  |
| ------------------------- | ------------------------------------------------------------------------- |

| Property                               | Pattern | Type        | Deprecated | Definition | Title/Description |
| -------------------------------------- | ------- | ----------- | ---------- | ---------- | ----------------- |
| - [title](#title )                     | No      | string      | No         | -          | News item         |
| - [pubDate](#pubDate )                 | No      | string      | No         | -          | News item         |
| - [link](#link )                       | No      | string      | No         | -          | News item         |
| - [description](#description )         | No      | Combination | No         | -          | News item         |

## <a name="title"></a>1. [Optional] Property `News item > title`

**Title:** News item

| Type                      | `string` or `null`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The title of the news item.

## <a name="pubDate"></a>2. [Optional] Property `News item > pubDate`

**Title:** News item

| Type                      | `string` or `null`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The date the news item was published.

## <a name="link"></a>3. [Optional] Property `News item > link`

**Title:** News item

| Type                      | `string` or `null`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The URL to the news item.

## <a name="description"></a>4. [Optional] Property `News item > description`

**Title:** News item

| Type                      | `combining` or `null`                                                     |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The description of the news item.

### <a name="description_text"></a>4.1. Property `News item > description > text`

**Title:** description

| Type                      | `string` or `null`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The text of the news item.

### <a name="description_link"></a>4.2. Property `News item > description > link`

**Title:** description

| Type                      | `array` or `null`                                                         |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** Other ULRs met in the description of the news item.

### <a name="description_images"></a>4.3. Property `News item > description > images`

**Title:** description

| Type                      | `array` or `null`                                                         |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The ULRs to the images met in the description of the news item.