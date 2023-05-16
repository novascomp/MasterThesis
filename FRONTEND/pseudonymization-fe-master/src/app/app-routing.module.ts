import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {LoginComponent} from './security/login/login.component';
import {CallbackComponent} from './security/callback/callback.component';
import {NotFoundComponent} from "./not-found/not-found.component";
import {MainComponent} from "./main/main.component";
import {AboutComponent} from "./about/about.component";

const routes: Routes = [
  {path: '', redirectTo: '/login', pathMatch: 'full'},
  {path: 'login', component: LoginComponent},
  {path: 'callback', component: CallbackComponent},
  {path: 'main', component: MainComponent},
  {path: 'oaplikaci', component: AboutComponent},
  {path: 'neplatny/pozadavek', component: NotFoundComponent},
  {path: '**', redirectTo: '/neplatny/pozadavek'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
