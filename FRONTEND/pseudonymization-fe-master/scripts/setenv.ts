//https://plainenglish.io/blog/setup-dotenv-to-access-environment-variables-in-angular-9-f06c6ffb86c0

const { writeFile } = require('fs');
const { argv } = require('yargs');

// read environment variables from .env file
require('dotenv').config();

// read the command line arguments passed with yargs
const environment = argv.environment;
const isProduction = environment === 'prod';

const targetPath = isProduction
  ? `./src/environments/environment.prod.ts`
  : `./src/environments/environment.ts`;

// we have access to our environment variables
// in the process.env object thanks to dotenv
const environmentFileContent = `
export const environment = {
   production: ${isProduction},
   pkcs11Service: "${process.env.PKCS11_SERVICE}",
   datGenService: "${process.env.DATGEN_SERVICE}",
   LOGOUT_REDIRECT_URI: "${process.env.LOGOUT_REDIRECT_URI}",
   LOGIN_REDIRECT_URI: "${process.env.LOGIN_REDIRECT_URI}"
};
`;

// write the content to the respective file
writeFile(targetPath, environmentFileContent, function (err) {
  if (err) {
    console.log(err);
  }

  console.log(`Wrote variables to ${targetPath}`);
})

const environment_dev = './src/environments/environment.ts';
writeFile(environment_dev, environmentFileContent, function (err) {
  if (err) {
    console.log(err);
  }

  console.log(`Wrote variables to ${targetPath}`);
})
