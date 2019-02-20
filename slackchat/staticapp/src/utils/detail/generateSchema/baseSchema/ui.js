import * as publishPathHelp from 'Content/detail/publishPathHelp';

export default (data = {}) => ({
  'chat_type': {
    'ui:help': 'Save a chat a type to show more options below.',
  },
  'published': {
    'ui:widget': 'toggle',
    'ui:help': 'Is the chat page published?',
  },
  'live': {
    'ui:widget': 'toggle',
    'ui:help': 'Is the chat still going on?',
  },
  'title': {

  },
  'introduction': {
    'ui:widget': 'textarea',
  },
  'publish_time': {
    'ui:widget': 'date-time',
    'ui:help': 'Setting a time in the future will not affect the chat\'s publish status.',
  },
  'publish_path': {
    'ui:help': window.DATA.published === true ? publishPathHelp.published : publishPathHelp.unpublished(data.chat_type),
    'ui:disabled': window.DATA.published === true,
  },
  'meta': {
    'title': {

    },
    'description': {

    },
    'image': {

    },
  },
});
