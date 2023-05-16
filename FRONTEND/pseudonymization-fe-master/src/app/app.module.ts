import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatGridListModule} from '@angular/material/grid-list';
import {MatCardModule} from '@angular/material/card';
import {MatButtonModule} from '@angular/material/button';
import {AppRoutingModule} from './app-routing.module';
import {LoginComponent} from './security/login/login.component';
import {MatBadgeModule} from '@angular/material/badge';
//import {DocumentUploaderComponent} from '../../../../../../../../Downloads/BachelorThesis-main/Frontend/vlastnik_Angular/src/app/uploaders/document-uploader/document-uploader.component';
import {MatInputModule} from '@angular/material/input';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatIconModule} from '@angular/material/icon';
import {MatDatepicker, MatDatepickerModule} from '@angular/material/datepicker';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatSelectModule} from '@angular/material/select';
import {MatNativeDateModule} from '@angular/material/core';
import {MatDialogModule} from '@angular/material/dialog';
import {MatToolbarModule} from '@angular/material/toolbar';
import {CallbackComponent} from './security/callback/callback.component';
import {HttpClientModule} from '@angular/common/http';
import {MatStepperModule} from '@angular/material/stepper';
import {FlexLayoutModule} from '@angular/flex-layout';
import {MatMenuModule} from '@angular/material/menu';
import {MatTableModule} from '@angular/material/table';
import {MatPaginatorModule} from '@angular/material/paginator';
import {MatSortModule} from '@angular/material/sort';
import {DragDropModule} from '@angular/cdk/drag-drop';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {NgxDropzoneModule} from 'ngx-dropzone';
import {MatProgressBarModule} from '@angular/material/progress-bar';
//import {MomentDateModule} from '@angular/material-moment-adapter';
import {MatTabsModule} from '@angular/material/tabs';
import {MatCheckboxModule} from '@angular/material/checkbox';
//import {RECAPTCHA_V3_SITE_KEY, RecaptchaV3Module} from 'ng-recaptcha';
import {NotFoundComponent} from './not-found/not-found.component';
import {MatTooltipModule} from '@angular/material/tooltip';
import {MainComponent} from './main/main.component';
import {DatgenTableComponent} from './datgen-table/datgen-table.component';
import {Pkcs11TableComponent} from './pkcs11-table/pkcs11-table.component';
import {AboutComponent} from './about/about.component';
import {MatChip, MatChipsModule} from "@angular/material/chips";
import {PseudStepperComponent} from "./pseud-stepper/pseud-stepper.component";
import {MatRadioModule} from "@angular/material/radio";

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    CallbackComponent,
    NotFoundComponent,
    MainComponent,
    DatgenTableComponent,
    Pkcs11TableComponent,
    AboutComponent,
    PseudStepperComponent,
  ],
  imports: [
    HttpClientModule,
    //  MomentDateModule,
    BrowserModule,
    BrowserAnimationsModule,
    MatGridListModule,
    MatCardModule,
    MatButtonModule,
    MatBadgeModule,
    MatInputModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatDatepickerModule,
    MatAutocompleteModule,
    MatSelectModule,
    MatNativeDateModule,
    MatDialogModule,
    MatToolbarModule,
    MatStepperModule,
    FlexLayoutModule,
    MatMenuModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    DragDropModule,
    MatProgressSpinnerModule,
    NgxDropzoneModule,
    MatProgressBarModule,
    MatTabsModule,
    MatCheckboxModule,
    //  RecaptchaV3Module,
    MatTooltipModule,
    AppRoutingModule,
    MatChipsModule,
    MatRadioModule,
  ],
  //providers: [{provide: RECAPTCHA_V3_SITE_KEY, useValue: ''}],
  providers: [],
  bootstrap: [AppComponent]

})
export class AppModule {
}
