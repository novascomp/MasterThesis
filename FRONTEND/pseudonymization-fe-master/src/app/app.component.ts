import {Component, enableProdMode, OnDestroy, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {OktaAuthService} from './security/okta-auth.service';
//import {OnExecuteData, ReCaptchaV3Service} from 'ng-recaptcha';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  start: boolean;
  isAuthenticated: boolean;

  private subscription: Subscription;

  constructor(public router: Router,
              public oktaAuth: OktaAuthService) {
  }

  ngOnInit(): void {
    this.oktaAuth.$isAuthenticated.subscribe(val => {
      this.isAuthenticated = val;
    });
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
}

//https://developer.okta.com/code/angular/okta_angular_auth_js/


