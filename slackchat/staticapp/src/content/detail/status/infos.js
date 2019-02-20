export const willPublish = path => ({
  statusText: `Clicking save will **PUBLISH** or **OVERWRITE** [this chat page](${path}/).`,
  statusLevel: 'info',
});

export const willNotPublish = path => ({
  statusText: `Clicking save will **DELETE** [this chat page](${path}/), if it exists.`,
  statusLevel: 'info',
});
