import isEmpty from 'lodash/isEmpty';
import getChatType from 'Utils/getChatType';

import DetailForm from './DetailForm';

const { ALL_CHAT_TYPES: allChatTypes } = window;

const customEnums = [
  {
    name: 'chat_type',
    data: allChatTypes.map(c => ({ label: c.name, value: c.id })),
  },
  {
    name: 'live',
    data: [
      { label: 'Yes', value: true },
      { label: 'No', value: false },
    ],
  },
];

export default (data = {}) => {
  const chatType = getChatType(data.chat_type);

  const noCustomSchema = isEmpty(chatType) || chatType.jsonSchema === null || chatType.uiSchema === null;
  const customSchemas = noCustomSchema ?
    [] :
    [{
      name: 'extras',
      data: chatType,
    }];

  const form = new DetailForm();

  customSchemas.forEach(s => {
    form.register(s.name, s.data);
  });

  customEnums.forEach(e => {
    form.enum(e.name, e.data);
  });

  form.update(data);

  return form.render();
};
