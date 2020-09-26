# -*- coding: utf-8 -*-
"""
    Copyright (C) 2020 Tubed (plugin.video.tubed)

    This file is part of plugin.video.tubed

    SPDX-License-Identifier: GPL-2.0-only
    See LICENSES/GPL-2.0-only.txt for more information.
"""

from html import unescape

from ..constants import MODES
from ..items.video import Video
from ..lib.url_utils import create_addon_path


def video_generator(items):
    for item in items:
        video_id = ''

        kind = item.get('kind', '')
        if not kind:
            continue

        snippet = item.get('snippet', {})
        if not snippet:
            continue

        if kind == 'youtube#video':
            video_id = item.get('id', '')

        elif kind == 'youtube#playlistItem':
            video_id = snippet.get('resourceId', {}).get('videoId', '')

        elif kind == 'youtube#searchResult':
            if isinstance(item.get('id', {}), dict):
                video_id = item.get('id', {}).get('videoId', '')

        if not video_id:
            continue

        payload = Video(
            label=unescape(snippet.get('title', '')),
            label2=unescape(snippet.get('channelTitle', '')),
            path=create_addon_path({
                'mode': str(MODES.PLAY),
                'video_id': video_id
            })
        )

        info_labels = {
            'mediatype': 'video',
            'plot': unescape(snippet.get('description', '')),
            'plotoutline': unescape(snippet.get('description', '')),
            'originaltitle': unescape(snippet.get('title', '')),
            'sorttitle': unescape(snippet.get('title', '')),
            'studio': unescape(snippet.get('channelTitle', ''))
        }
        payload.ListItem.setInfo('video', info_labels)

        thumbnails = snippet.get('thumbnails', {})
        thumbnail = thumbnails.get('standard', thumbnails.get('high', {}))
        if not thumbnail:
            thumbnail = thumbnails.get('medium', thumbnails.get('default', {}))
        thumbnail = thumbnail.get('url', '')

        payload.ListItem.setArt({
            'icon': thumbnail,
            'thumb': thumbnail,
        })

        yield tuple(payload)