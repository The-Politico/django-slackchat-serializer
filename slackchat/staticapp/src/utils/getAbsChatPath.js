import path from 'path';
import getContentByName from 'Utils/getContentByName';
import getChatType from 'Utils/getChatType';
import parseURL from 'Utils/parseURL';

export default data => {
  const publishRoot = parseURL(getContentByName('PUBLISH_ROOT'));
  const chatType = getChatType(data.chat_type);
  return chatType && data.publish_path ? `${publishRoot.protocol}//` + path.join(publishRoot.hostname, publishRoot.pathname, chatType.publish_path, data.publish_path) : null;
};
