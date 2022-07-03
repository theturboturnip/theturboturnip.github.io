'use strict';

const
    fs = require('fs'),
    handlebars = require('handlebars'),
    handlebarsWax = require('handlebars-wax'),
    addressFormat = require('address-format'),
    moment = require('moment'),
    Swag = require('swag');

Swag.registerHelpers(handlebars);

handlebars.registerHelper({
    removeProtocol: function (url) {
        return url.replace(/.*?:\/\//g, '');
    },

    concat: function() {
        let res = '';

        for(let arg in arguments){
            if (typeof arguments[arg] !== 'object') {
                res += arguments[arg];
            }
        }

        return res;
    },

    formatAddress: function(address, city, region, postalCode, countryCode) {
        let addressList = addressFormat({
            address: address,
            city: city,
            subdivision: region,
            postalCode: postalCode,
            countryCode: countryCode
        });


        return addressList.join('<br/>');
    },

    formatDate: function(date) {
        // If only a year is specified, don't add a month
        if (date.match(/^[0-9]+$/)) {
            return moment(date).format('YYYY');
        } else {
            return moment(date).format('MM/YYYY');
        }
    },

    ifEquals: function(arg1, arg2, options) {
        return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
    }
});


function render(resume) {
    let dir = __dirname + '/public',
        css = fs.readFileSync(dir + '/styles/main.css', 'utf-8'),
        resumeTemplate = fs.readFileSync(dir + '/views/resume.hbs', 'utf-8');

    let Handlebars = handlebarsWax(handlebars);

    Handlebars.partials(dir + '/views/partials/**/*.{hbs,js}');
    Handlebars.partials(dir + '/views/components/**/*.{hbs,js}');

    return Handlebars.compile(resumeTemplate)({
        css: css,
        resume: resume
    });
}

// From https://github.com/jsonresume/resume-cli/issues/617
module.exports = {
	render: render,
	pdfRenderOptions: {
		format: 'A4',
		mediaType: 'print',
		pdfViewport: { width: 1920, height: 1280 },
		margin: {
			top: '0.2in',
			bottom: '0.2in',
			left: '0.4in',
			right: '0.4in',
		},
	},
};