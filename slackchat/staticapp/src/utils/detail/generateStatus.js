import getAbsChatPath from 'Utils/getAbsChatPath';

import * as statuses from 'Content/detail/status';

export default (data) => {
  let newStatus = { statusText: '', statusLevel: null };

  const fullPublishPath = getAbsChatPath(data);

  if (fullPublishPath) {
    if (data.published) {
      newStatus = statuses.info.willPublish(fullPublishPath);
    } else {
      newStatus = statuses.info.willNotPublish(fullPublishPath);
    }
  }

  return newStatus;
};
