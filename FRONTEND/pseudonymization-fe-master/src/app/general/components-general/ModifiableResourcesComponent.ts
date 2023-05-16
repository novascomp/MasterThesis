import {RestGeneralResponse} from "src/app/rest/response/RestGeneralResponse";
import {GeneralComponentTitles} from "../enum/titles/GeneralComponentTitles";

export class ModifiableResourcesComponent {

  serverUnavailable: boolean;
  badRequest: boolean;
  unauthorized: boolean;
  notFound: boolean;
  notPermitted: boolean;
  alreadyRegistered: boolean;
  internalException: boolean;
  serviceUnavailable: boolean;
  recaptchaFailed: boolean;

  errorText: string;

  constructor() {
    this.initGlobal();
  }

  public initGlobal(): void {
    this.serverUnavailable = false;
    this.badRequest = false;
    this.unauthorized = false;
    this.notFound = false;
    this.notPermitted = false;
    this.alreadyRegistered = false;
    this.internalException = false;
    this.serviceUnavailable = false;
    this.recaptchaFailed = false;
    this.errorText = null;
  }

  public handleError(restGeneralResponse: RestGeneralResponse): void {

    if (restGeneralResponse === RestGeneralResponse.serverUnavailable) {
      this.serverUnavailable = true;
      this.errorText = this.getUnavailableText();
    } else if (restGeneralResponse === RestGeneralResponse.badRequest) {
      this.badRequest = true;
      this.errorText = this.getBadRequestText();
    } else if (restGeneralResponse === RestGeneralResponse.unauthorized) {
      this.unauthorized = true;
      this.errorText = this.getUnauthorizedText();
    } else if (restGeneralResponse === RestGeneralResponse.notFound) {
      this.notFound = true;
      this.errorText = this.getNotFoundText();
    } else if (restGeneralResponse === RestGeneralResponse.notPermitted) {
      this.notPermitted = true;
      this.errorText = this.getNotPermittedText();
    } else if (restGeneralResponse === RestGeneralResponse.alreadyRegistered) {
      this.alreadyRegistered = true;
      this.errorText = this.getConflictFailedText();
    } else if (restGeneralResponse === RestGeneralResponse.serviceUnavailable) {
      this.serviceUnavailable = true;
      this.errorText = this.getUnavailableText();
    } else if (restGeneralResponse === RestGeneralResponse.internalException) {
      this.internalException = true;
      this.errorText = this.getInternalErrorText();
    }
  }

  public getErrorText(): string {
    return this.errorText;
  }

  public getUnavailableText(): string {
    return GeneralComponentTitles.UNAVAILABLE;
  }

  public getNotPermittedText(): string {
    return GeneralComponentTitles.NOT_PERMITTED;
  }

  public getUnauthorizedText(): string {
    return GeneralComponentTitles.UNAUTHORIZED;
  }

  public getNotFoundText(): string {
    return GeneralComponentTitles.NOT_FOUND;
  }

  public getBadRequestText(): string {
    return GeneralComponentTitles.BAD_REQUEST;
  }

  public getConflictFailedText(): string {
    return GeneralComponentTitles.CONFLICT;
  }

  public getInternalErrorText(): string {
    return GeneralComponentTitles.INTERNAL_ERROR;
  }

  public getInvalidOperation(): string {
    return GeneralComponentTitles.INVALID_REQUEST;
  }
}
