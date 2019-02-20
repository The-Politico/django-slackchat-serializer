import path from 'path';
import getContentByName from 'Utils/getContentByName';

export default data => {
  const root = getContentByName('SLACK_TEAM_ROOT');

  return data.api_id ? path.join(root, 'messages', data.api_id) : null;
};
