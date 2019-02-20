import path from 'path';
import getChatType from 'Utils/getChatType';
import getContentByName from 'Utils/getContentByName';

export default chatType => {
  const defaultValue = '/chat-type-publish-root/';
  const chatTypePath = chatType ? getChatType(chatType).publish_path : defaultValue;
  const publishRoot = getContentByName('PUBLISH_ROOT');
  const publishPath = path.join(publishRoot, chatTypePath);

  return `The part of the URL after "${publishPath}".`;
};
