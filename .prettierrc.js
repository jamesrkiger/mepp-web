module.exports = {
  singleQuote: true,
  trailingComma: 'all',
  quoteProps: 'preserve',
  experimentalBabelParserPluginsList: ['jsx'],
  importOrder: [
    '^@material-ui/(.*)$',
    '^@admin/(.*)$',
    '^@assets/(.*)$',
    '^@styles/(.*)$',
    '^@themes/(.*)$',
    '^@pages/(.*)$',
    '^@hocs/(.*)$',
    '^@hooks/(.*)$',
    '^@providers/(.*)$',
    '^@utils/(.*)$',
    '^@layouts/(.*)$',
    '^@components/(.*)$',
    '^[./]',
    'mirror',
  ],
  importOrderSeparation: true,
};