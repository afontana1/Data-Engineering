# SaaS Starter: Front End

This repository holds the front-end code for the SaaS-starter site. It relies on the API in the infrastructure stack being deployed already. The site is serverless, using a Gatsby to statically render some pages, but React to also provide auth-gated interaction.

View the live example at: [SaaS Starter Stack](https://saas-starter-stack.com/)

## Development

```bash
# Run the site on a development server locally.
gatsby develop

# Visit http://127.0.0.1:8000 (localhost and 0.0.0.0 will have some problems with navigation)
```

### Configuration

1. Configure the`.env.development` and `.env.production` with the endpoints and meta-data. Make sure that secret keys and configuration aren't committed to the git!
2. Configure the S3 bucket and CloudFront `distribution_id` in `package.json`.

### Tech Stack

* **[React](https://reactjs.org/)**: Front-end framework
* **[Gatsby](https://www.gatsbyjs.com/)**: Static rendering framework
* **[Tailwind CSS](https://tailwindcss.com/)**: Styling framework
* **[FontAwesome](https://fontawesome.com/)**: Icon fonts

## Deployment

The site must be built and deployed to S3. We then have to invalidate the CloudFront caches so the CDN gets the latest version of the site. This assumes that the infrastructure has already been deployed to your AWS account.

The full deployment commands are:

```bash
npm run build
aws s3 sync public s3://<your-domain>.com/ --acl public-read
aws cloudfront create-invalidation --distribution-id XXXXXXXX --paths \"/*\""
```

But you can also use the `full-deploy` command that does all three:

```bash
npm run full-deploy
```

## Testing

I've only written tests for the API integration (for each of the API files). To run it for a particular file:

```bash
jest AuthApi.test.ts
```

To test a particular case:

```bash
jest AuthApi.test.ts -t "can reset account"
```

**Note**: You may need to this run these tests from the root (this) directory because it attempts to load environment variables from `.env.development`.

## Notes

* An issue that puzzled me for a while was due to something called re-hydration. It happens when Gatsby renders a static version of the site, but then the React logic updates something after. The result is a Frankenstein `div` that has mixed styling. To fix this, I used a hook that updates the `key` of `div`s that must change after static loading. See `useRenderKey.ts`.
