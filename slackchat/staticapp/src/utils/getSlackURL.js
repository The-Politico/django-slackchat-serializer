import path from 'path';
import getContentByName from 'Utils/getContentByName';
import parseURL from 'Utils/parseURL';

export default data => {
  const root = parseURL(getContentByName('SLACK_TEAM_ROOT'));
  return data.api_id ? `${root.protocol}//` + path.join(root.hostname, root.pathname, 'messages', data.api_id) : null;
};
