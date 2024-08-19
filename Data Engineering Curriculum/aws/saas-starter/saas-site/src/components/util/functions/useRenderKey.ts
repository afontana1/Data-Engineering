import { useState, useEffect } from "react";

interface RenderKey {
  isClient: boolean;
  key: string;
}

const useRenderKey = (): RenderKey => {
  const [isClient, setClient] = useState(false);
  const key = isClient ? "client" : "server";

  useEffect(() => {
    setClient(true);
  }, []);

  return { isClient, key };
};

export default useRenderKey;
