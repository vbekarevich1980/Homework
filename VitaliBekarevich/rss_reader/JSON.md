###### **JSON form used in the rss_reader utility**

`{
    "feed": "RSS feed channel title",
    "feed_url": "RSS feed URL",
    "title": "News item title",
    "pubDate": "News publishing date",
    "link": "News item URL",
    "description": 
        {
            "text": "News item text",
            "links": ["News item additional URLs"],
            "images": ["News item images URLs"],
        },
}`


# News item

- [1. Property `News item > feed`](#feed)
- [2. Property `News item > feed_url`](#feed_url)
- [3. [Optional] Property `News item > title`](#title)
- [4. [Optional] Property `News item > pubDate`](#pubDate)
- [5. [Optional] Property `News item > link`](#link)
- [6. [Optional] Property `News item > description`](#description)
  - [6.1. Property `News item > description > text`](#description_text)
  - [6.2. Property `News item > description > links`](#description_links)
  - [6.3. Property `News item > description > images`](#description_images)

**Title:** News item

| Type                      | `object`                                                                  |
| ------------------------- | ------------------------------------------------------------------------- |

| Property                               | Pattern | Type        | Deprecated | Definition | Title/Description |
| -------------------------------------- | ------- | ----------- | ---------- | ---------- | ----------------- |
| - [feed](#feed )                       | No      | string      | No         | -          | News item         |
| - [feed_url](#feed_url )               | No      | string      | No         | -          | News item         |
| - [title](#title )                     | No      | string      | No         | -          | News item         |
| - [pubDate](#pubDate )                 | No      | string      | No         | -          | News item         |
| - [link](#link )                       | No      | string      | No         | -          | News item         |
| - [description](#description )         | No      | Combination | No         | -          | News item         |

## <a name="feed"></a>1. Property `News item > feed`

**Title:** News item

| Type                      | `string`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The title of the RSS feed channel.

## <a name="feed_url"></a>2. Property `News item > feed_url`

**Title:** News item

| Type                      | `string`                                                       |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The URL of the RSS feed.

## <a name="title"></a>3. [Optional] Property `News item > title`

**Title:** News item

| Type                      | `string` or `null`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The title of the news item.

## <a name="pubDate"></a>4. [Optional] Property `News item > pubDate`

**Title:** News item

| Type                      | `string` or `null`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The date the news item was published.

## <a name="link"></a>5. [Optional] Property `News item > link`

**Title:** News item

| Type                      | `string` or `null`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The URL to the news item.

## <a name="description"></a>6. [Optional] Property `News item > description`

**Title:** News item

| Type                      | `combining` or `null`                                                     |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The description of the news item.

### <a name="description_text"></a>6.1. Property `News item > description > text`

**Title:** description

| Type                      | `string` or `null`                                                        |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The text of the news item.

### <a name="description_link"></a>6.2. Property `News item > description > link`

**Title:** description

| Type                      | `array` or `null`                                                         |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** Other ULRs met in the description of the news item.

### <a name="description_images"></a>6.3. Property `News item > description > images`

**Title:** description

| Type                      | `array` or `null`                                                         |
| ------------------------- | ------------------------------------------------------------------------- |

**Description:** The ULRs to the images met in the description of the news item.