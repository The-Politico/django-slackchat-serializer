export default (data = {}) => ({
  'type': 'object',
  'required': [
    'chat_type',
    'publish_path',
    'title',
    'introduction',
  ],
  'properties': {
    'published': {
      'type': 'boolean',
      'title': 'Publish Status',
    },
    'live': {
      'type': 'boolean',
      'title': 'Live',
    },
    'chat_type': {
      'type': 'integer',
      'title': 'Chat Type',
    },
    'title': {
      'type': 'string',
      'title': 'Title',
    },
    'introduction': {
      'type': 'string',
      'title': 'Introduction',
    },
    'publish_time': {
      'type': 'string',
      'title': 'Publish Time',
    },
    'publish_path': {
      'type': 'string',
      'title': 'URL Path',
      'pattern': `^[A-z/\\-_]*$`,
    },
    'meta': {
      'type': 'object',
      'title': 'SEO',
      'properties': {
        'title': {
          'type': 'string',
          'title': 'Title',
        },
        'description': {
          'type': 'string',
          'title': 'Description',
        },
        'image': {
          'type': 'string',
          'title': 'Image',
        },
      },
    },
  },
});
