const withSideEffect = <T>(
  p: Promise<T>,
  executor: (x: T) => void
): Promise<T> => {
  return new Promise<T>((resolve, reject) => {
    p.then((r: T) => {
      executor(r);
      resolve(r);
    }).catch(reject);
  });
};

export default withSideEffect;
