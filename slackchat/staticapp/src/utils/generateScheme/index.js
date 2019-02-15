import DetailForm from './DetailForm';
import isEmpty from 'lodash/isEmpty';

const { CHAT_DATA: chatData, ALL_CHAT_TYPES: allChatTypes } = window;

const getSchema = (form, data, schemas = [], enums = []) => {
  form.update(data);

  schemas.forEach(s => {
    form.register(s.name, s.data);
  });

  enums.forEach(e => {
    form.enum(e.name, e.data);
  });

  console.log('form-render', form.render());

  return form.render();
};

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

export default chatType => {
  const noCustomSchema = isEmpty(chatType) || chatType.jsonSchema === null || chatType.uiSchema === null;
  const customSchemas = noCustomSchema ?
    [] :
    [{
      name: 'extras',
      data: chatType,
    }];

  const form = new DetailForm();
  return getSchema(form, chatData, customSchemas, customEnums);
};
