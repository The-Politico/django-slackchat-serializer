import path from 'path';
import getContentByName from 'Utils/getContentByName';
import getChatType from 'Utils/getChatType';

export default data => {
  const publishRoot = getContentByName('PUBLISH_ROOT');
  const chatType = getChatType(data.chat_type);

  return chatType && data.publish_path ? path.join(publishRoot, chatType.publish_path, data.publish_path) : null;
};
