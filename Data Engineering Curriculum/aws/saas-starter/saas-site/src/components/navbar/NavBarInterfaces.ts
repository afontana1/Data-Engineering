export interface NavMenuItem {
  label: string;
  action: any;
}

export interface NavMenuCommonProps {
  profileName: string;
  isMobile?: boolean;
  isShowing?: boolean;
  setIsShowing?: (x: boolean) => void;
  wrapperRef?: any;
  items: NavMenuItem[];
}
