'use strict';

const
    fs = require('fs'),
    handlebars = require('handlebars'),
    handlebarsWax = require('handlebars-wax'),
    addressFormat = require('address-format'),
    moment = require('moment'),
    Swag = require('swag'),
    Filter = require("handlebars.filter"),
    resolve = require('path').resolve;

Swag.registerHelpers(handlebars);
Filter.registerHelper(handlebars);

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

    ifEquals: function(arg1, arg2, options) {
        return (arg1 == arg2) ? options.fn(this) : options.inverse(this);
    },

    orIfNull: function(arg1, arg2) {
        if (arg1) {
            return arg1;
        }
        return arg2;
    },

    yearsAgo: function(year) {
        let years = new Date().getFullYear() - year;
        if (years == 1) {
            return "1 year";
        } else {
            return years + " years";
        }
    },

    nYears: function(years) {
        if (years == 1) {
            return "1 year";
        } else {
            return years + " years";
        }
    },

    authorString: function(authors) {
        if (authors) {
            let authorStr = "First author: " + authors[0];
            let otherAuthors = authors.slice(1);
            if (otherAuthors.length > 0) {
                authorStr += "; Co-authors: ";
                let first = true;
                otherAuthors.forEach((author) => {
                    if (!first) {
                        authorStr += ", ";
                    }
                    authorStr += author;
                    first = false;
                });
            }
            return authorStr;
        } else {
            return "";
        }
    },

    subset: function(array, start, end) {
        if (start == null) {
            return array;
        }
        if (end == null) {
            return array.slice(start);
        }
        return array.slice(start, end);
    }
});


function render(resume) {
    let dir = __dirname + '/public',
        css = fs.readFileSync(dir + '/styles/main.css', 'utf-8'),
        resumeTemplate = fs.readFileSync(dir + '/views/resume.hbs', 'utf-8');

    let Handlebars = handlebarsWax(handlebars);

    Handlebars.partials(dir + '/views/partials/**/*.{hbs,js}');
    Handlebars.partials(dir + '/views/components/**/*.{hbs,js}');

    if (resume.special) {
        handlebars.registerPartial("special", fs.readFileSync(dir + '/views/specials/' + resume.special + '.hbs', 'utf-8'));
    }

    handlebars.registerHelper("imagedata", (arg) => {
        // let str = fs.readFileSync(__dirname + '/../assets/kiryu-yk-gmd-io-smaller.png').toString("base64");

        // This embeds the image directly - need to make sure it's small, or puppeteer craps out.
        // TODO how to get this to work differently with html?
        let str = fs.readFileSync(__dirname + '/../assets/' + arg).toString("base64");        
        str = "data:image/" + arg.split(".")[1] + ';base64,' + str;
        return str;

        // // Doesn't work with puppeteer
        // // https://stackoverflow.com/q/66751136
        // return 'file://' + resolve(__dirname + '/../assets/' + arg);
    });

    if (resume.jp_date) {
        handlebars.registerHelper({
            formatDate: function(date) {
                // If only a year is specified, don't add a month
                if (date.match(/^[0-9]+$/)) {
                    return moment(date).format('YYYY');
                } else {
                    return moment(date).format('YYYY-MM');
                }
            },
        });
    } else {
        handlebars.registerHelper({
            formatDate: function(date) {
                // If only a year is specified, don't add a month
                if (date.match(/^[0-9]+$/)) {
                    return moment(date).format('YYYY');
                } else {
                    return moment(date).format('MMMM YYYY');
                }
            },
        });
    }

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