import {CryptoService} from "./crypto.service";
import {EncryptHTTPS} from "../model/encrypt/EncryptHTTPS";

export abstract class PseudonymizationService<T> extends CryptoService<T> {

  public abstract pseudonymize(model: EncryptHTTPS);
}
