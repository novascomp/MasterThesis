import {Component, OnInit, ViewChild} from '@angular/core';
import {MatPaginator} from "@angular/material/paginator";
import {MatTabChangeEvent} from "@angular/material/tabs";

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {

  serverUnavailable: boolean;
  unauthorized: boolean;

  loaded: boolean;

  currentTabIndex: number;
  fileSource: string;
  pseudFormActivated: boolean;

  @ViewChild(MatPaginator) paginator: MatPaginator;


  constructor() {
    this.pseudFormActivated = false
  }

  async ngOnInit() {
    this.currentTabIndex = 0
    this.loaded = true;
  }

  pseudEmitted(event): void {
    this.pseudFormActivated = true
    this.currentTabIndex = 2
    this.fileSource = event
    console.log(event)
  }

  pseudFormSubmitted(event): void {
    this.currentTabIndex = 0
    this.pseudFormActivated = false
    console.log(event)
  }

  public tabChanged(tabChangeEvent: MatTabChangeEvent): void {
    this.currentTabIndex = tabChangeEvent.index;
  }
}
