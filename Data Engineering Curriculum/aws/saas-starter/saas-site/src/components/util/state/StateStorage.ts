class StateStorage {
  private readonly storageKey: string;
  private readonly isBrowser: boolean = typeof window !== "undefined";

  constructor(key: string) {
    this.storageKey = key;
  }

  public save(serializedState: string) {
    if (this.isBrowser) {
      window.localStorage.setItem(this.storageKey, serializedState);
      console.log(`Saved Local State: ${serializedState}`);
    }
  }

  public load(): any {
    const isBrowser = typeof window !== "undefined";
    if (isBrowser) {
      const sessionString = window.localStorage.getItem(this.storageKey);
      if (sessionString !== null && sessionString.length > 0) {
        console.log(`Loading state from memory: ${sessionString}`);
        return JSON.parse(sessionString);
      }
    }

    return null;
  }

  public clear(): void {
    if (this.isBrowser) {
      window.localStorage.removeItem(this.storageKey);
    }
  }
}

export default StateStorage;
