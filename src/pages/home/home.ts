import { Component, OnInit } from "@angular/core";
import {
  NavController,
  LoadingController,
  AlertController,
} from "ionic-angular";

import { FormGroup, FormControl, Validators } from "@angular/forms";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { InAppBrowser } from '@ionic-native/in-app-browser/ngx';

// import {} from '@angukla='
@Component({
  selector: "page-home",
  templateUrl: "home.html"
})
export class HomePage implements OnInit {
  newsForm: FormGroup;
  validLength = 0;
  predictionPercentage = 0;
  show = false;
  ip = "localhost";
  sites_url = []

  constructor(
    public navCtrl: NavController,
    private http: HttpClient,
    private loadingCtrl: LoadingController,
    private alertCtrl: AlertController,
    private iab: InAppBrowser
  )
   {}
  ngOnInit() {
    this.newsForm = new FormGroup({
      text: new FormControl("", [Validators.required])
    });
    console.log([
      this.newsForm,
      this.newsForm.value.text.trim().length,
      !this.newsForm.valid && this.newsForm.value.text.trim().length !== 0
    ]);
    this.newsForm.get("text").valueChanges.subscribe(val => {
      this.validLength = val.trim().length;
    });
  }

  submit() {
    // this.showPrompt().then(() => {
      console.log(this.newsForm.value);
      this.show = false
      const loader = this.loadingCtrl.create({
        content: "Please wait while we analyse..."
      });
      const header = new HttpHeaders();
      header.set("Content-Type", "application/json");
      loader.present();
      console.log( {content:this.newsForm.get('text').value});
      
      this.http
        .post(`http://${this.ip}:5000/check-news`, {content:this.newsForm.get('text').value}, {
          headers: header
        })
        .subscribe(
          result => {
            // console.log(result);
            this.predictionPercentage = result["similarity"];
            this.sites_url = result["links"];
            this.show = true;
            loader.dismiss();
          },
          error => {
            alert('Internal server error occured , please try again later');
            // this.predictionPercentage = Math.floor(Math.random()*(100-50+1)+40);
            // this.predictionPercentage = 100
            this.show = false;
            loader.dismiss();
          }
        );
    // });
  }
  showPrompt() {
    return new Promise(resolve => {
      const prompt = this.alertCtrl.create({
        title: "Enter Ip address",
        message: "Enter server ip address",
        inputs: [
          {
            name: "ip",
            placeholder: "IP Adddress"
          }
        ],
        buttons: [
          {
            text: "Save",
            handler: data => {
              console.log(data);
              if (data.ip.length === 0) {
                resolve();
              } else {
                this.ip = data.ip;
                resolve();
              }
            }
          }
        ]
      });
      prompt.present();
    });
  }


  openBrowser(item){

    

    const browser = this.iab.create(item);

    browser.on('loadstop')

    // browser.close();
}

}
