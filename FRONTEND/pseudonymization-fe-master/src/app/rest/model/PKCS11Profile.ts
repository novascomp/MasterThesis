import {Profile} from "./Profile";

export class PKCS11Profile extends Profile {
  key_label: string;
  encryption_location: string;
  pseud_operation: string;
  technology: string;
  status: string;

  start: number;

  end: number;
}
