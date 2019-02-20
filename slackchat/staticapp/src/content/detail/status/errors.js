export const generic = err => ({
  statusText: `Something went wrong. ${err.toString()}`,
  statusLevel: 'error',
});

export const server = err => ({
  statusText: err,
  statusLevel: 'error',
});
