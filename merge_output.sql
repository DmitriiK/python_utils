CREATE TABLE [dbo].[Russell2_Stg_Company_tbl] (
    [companyName]          VARCHAR (100) NOT NULL,
    [tickerSymbol]         VARCHAR (35)  NULL,
    [companyId]            INT           NOT NULL,
    [yearFounded]          INT           NULL,
    [companyTypeId]        SMALLINT      NOT NULL,
    [units]                TINYINT       NULL,
    [monthFounded]         INT           NULL,
    [dayFounded]           INT           NULL,
    [PrimarySubTypeId]     INT           NULL,
    [exchangeId]           INT           NULL,
    [companyNameStartDate] SMALLDATETIME NULL,
    CONSTRAINT [PK_Russell2_Stg_Company_tbl] PRIMARY KEY CLUSTERED ([companyId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_CompositePortfolioToPortfolio_tbl] (
    [compositePortfolioToPortfolioId] INT            NOT NULL,
    [compositePortfolioId]            INT            NOT NULL,
    [portfolioId]                     INT            NOT NULL,
    [weight]                          NUMERIC (9, 5) NULL,
    CONSTRAINT [PK_Russell2_Stg_CompositePortfolioToPortfolio_tbl] PRIMARY KEY CLUSTERED ([compositePortfolioToPortfolioId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_ConstituentDates_tbl] (
    [constituentId] INT           NOT NULL,
    [readingDate]   SMALLDATETIME NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_ConstituentDates_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC, [readingDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_ConstituentIdentifier_tbl] (
    [constituentId]    INT            NOT NULL,
    [identifierTypeId] TINYINT        NOT NULL,
    [fromDate]         DATETIME       NOT NULL,
    [identifierValue]  NVARCHAR (300) NOT NULL,
    [toDate]           DATETIME       NULL,
    CONSTRAINT [PK_Russell2_Stg_ConstituentIdentifier_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC, [identifierTypeId] ASC, [fromDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_ConstituentToIndex_tbl] (
    [constituentId] INT NOT NULL,
    [indexId]       INT NOT NULL,
    [tradingItemId] INT NULL
);


GO
CREATE CLUSTERED INDEX [IX_Russell2_Stg_ConstituentToIndex_tbl]
    ON [dbo].[Russell2_Stg_ConstituentToIndex_tbl]([constituentId] ASC);


GO
CREATE TABLE [dbo].[Russell2_Stg_Constituent_tbl] (
    [constituentId] INT NOT NULL,
    [securityId]    INT NULL,
    [tradingItemId] INT NULL,
    [currencyId]    INT NULL,
    CONSTRAINT [PK_Russell2_Stg_Constituent_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_DataItem_Index_tbl] (
    [dataItemId]       INT          NOT NULL,
    [dataItemTag]      VARCHAR (20) NULL,
    [indexLevelTypeId] TINYINT      NULL,
    CONSTRAINT [PK_Russell2_Stg_DataItem_Index_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_DatesProcessing_tbl] (
    [bestPriceDate] SMALLDATETIME NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_DatesProcessing_tbl] PRIMARY KEY CLUSTERED ([bestPriceDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_ExchangeHoliday_tbl] (
    [holidayDate] SMALLDATETIME NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_ExchangeHoliday_tbl] PRIMARY KEY CLUSTERED ([holidayDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IdentifierType_tbl] (
    [identifierTypeId] TINYINT        NOT NULL,
    [identifierName]   NVARCHAR (100) NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_IdentifierType_tbl] PRIMARY KEY CLUSTERED ([identifierTypeId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexConstituentValue_Value112119_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      SMALLDATETIME    NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] INT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexConstituentValue_Value112119_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexConstituentValue_Value112120_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      SMALLDATETIME    NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] INT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexConstituentValue_Value112120_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexConstituentValue_Value112121WithSum_tbl] (
    [indexId]            INT              NOT NULL,
    [valueDate]          SMALLDATETIME    NOT NULL,
    [portfolioMarketCap] NUMERIC (38, 17) NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexConstituentValue_Value112121WithSum_tbl] PRIMARY KEY CLUSTERED ([indexId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexConstituentValue_Value112121_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      SMALLDATETIME    NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] INT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexConstituentValue_Value112121_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexConstituent_tbl] (
    [indexID]       INT      NOT NULL,
    [constituentID] INT      NOT NULL,
    [fromDate]      DATETIME NOT NULL,
    [toDate]        DATETIME NULL,
    [tradingItemId] INT      NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexConstituent_tbl] PRIMARY KEY CLUSTERED ([indexID] ASC, [constituentID] ASC, [fromDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexCorporateAction_tbl] (
    [indexID]       INT              NOT NULL,
    [constituentID] INT              NOT NULL,
    [seqID]         BIGINT           NOT NULL,
    [ICATypeId]     TINYINT          NOT NULL,
    [valueDate]     DATETIME         NOT NULL,
    [dataItemId]    INT              NOT NULL,
    [numericValue]  NUMERIC (38, 14) NULL,
    [textValue]     VARCHAR (200)    NULL,
    [tradingItemId] INT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexCorporateAction_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexID] ASC, [constituentID] ASC, [seqID] ASC, [ICATypeId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexExtended_tbl] (
    [indexObjectId]         INT      NOT NULL,
    [dataVendorId]          SMALLINT NOT NULL,
    [dealtrackEditableFlag] BIT      NOT NULL,
    [newTearsheetFlag]      BIT      NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexExtended_tbl] PRIMARY KEY CLUSTERED ([indexObjectId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexHistory_tbl] (
    [indexCompanyid] INT           NOT NULL,
    [effectiveDate]  SMALLDATETIME NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexHistory_tbl] PRIMARY KEY CLUSTERED ([indexCompanyid] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexICAType_tbl] (
    [ICATypeId]      TINYINT       NOT NULL,
    [ICAType]        VARCHAR (30)  NOT NULL,
    [ICADescription] VARCHAR (100) NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexICAType_tbl] PRIMARY KEY CLUSTERED ([ICATypeId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexProvider_tbl] (
    [indexProviderId]   SMALLINT     NOT NULL,
    [indexProviderName] VARCHAR (60) NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexProvider_tbl] PRIMARY KEY CLUSTERED ([indexProviderId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexRel_tbl] (
    [compositeIndexID] INT NOT NULL,
    [indexID]          INT NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexRel_tbl] PRIMARY KEY CLUSTERED ([compositeIndexID] ASC, [indexID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value106368_106370_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value106368_106370_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value113152_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value113152_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value113153_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value113153_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value113154_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value113154_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value114893_114896_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value114893_114896_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value601835_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value601835_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value601836_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value601836_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value601837_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value601837_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityTextCurrent_Value601838_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityTextCurrent_Value601838_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112032_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112032_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112033_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112033_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112034_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112034_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112109_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112109_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112110_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112110_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112111_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112111_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112112_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112112_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112113_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112113_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112114_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112114_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112115_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112115_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112117_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112117_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_Value112118_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_Value112118_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexSecurityValue_ValueOther_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexSecurityValue_ValueOther_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexToFeedType_tbl] (
    [feedTypeId]     SMALLINT      NOT NULL,
    [indexCompanyId] INT           NOT NULL,
    [inceptionDate]  SMALLDATETIME NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexToFeedType_tbl] PRIMARY KEY CLUSTERED ([indexCompanyId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexTradingItem_tbl] (
    [IndexId]           INT     NOT NULL,
    [tradingItemId]     INT     NOT NULL,
    [tradingItemTypeId] TINYINT NOT NULL,
    [currencyId]        INT     NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexTradingItem_tbl] PRIMARY KEY CLUSTERED ([tradingItemId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexValue_Value112099_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexValue_Value112099_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexValue_Value112100_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexValue_Value112100_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexValue_Value112102_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexValue_Value112102_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexValue_Value112103_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexValue_Value112103_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexValue_Value112106_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexValue_Value112106_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_IndexValue_ValueOther_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_Russell2_Stg_IndexValue_ValueOther_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_Index_tbl] (
    [indexID]         INT           NOT NULL,
    [indexProviderId] SMALLINT      NOT NULL,
    [indexName]       VARCHAR (255) NULL,
    [inceptionDate]   SMALLDATETIME NULL,
    CONSTRAINT [PK_Russell2_Stg_Index_tbl] PRIMARY KEY CLUSTERED ([indexID] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_PortfolioHoldingSymbol_tbl] (
    [constituentId]    INT            NOT NULL,
    [identifierTypeId] TINYINT        NULL,
    [fromDate]         SMALLDATETIME  NULL,
    [identifierValue]  NVARCHAR (300) NOT NULL,
    [toDate]           SMALLDATETIME  NULL,
    [holdingSymbolId]  INT            NOT NULL
);


GO
CREATE TABLE [dbo].[Russell2_Stg_PortfolioHolding_tbl] (
    [constituentId]       INT NOT NULL,
    [securityId]          INT NULL,
    [tradingItemId]       INT NULL,
    [currencyId]          INT NOT NULL,
    [cachedTradingItemId] INT NULL,
    CONSTRAINT [PK_Russell2_Stg_PortfolioHolding_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_PortfolioSnapshot_tbl] (
    [indexId]           INT              NOT NULL,
    [constituentId]     INT              NOT NULL,
    [fromDate]          SMALLDATETIME    NOT NULL,
    [toDate]            SMALLDATETIME    NOT NULL,
    [sharesOutstanding] DECIMAL (38, 16) NOT NULL,
    [tradingItemId]     INT              NULL,
    CONSTRAINT [PK_Russell2_Stg_PortfolioSnapshot_tbl] PRIMARY KEY CLUSTERED ([indexId] ASC, [constituentId] ASC, [fromDate] ASC, [toDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_Portfolio_tbl] (
    [portfolioId] INT      NOT NULL,
    [objectId]    INT      NOT NULL,
    [currencyId]  SMALLINT NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_Portfolio_tbl] PRIMARY KEY CLUSTERED ([portfolioId] ASC, [objectId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_PriceIndexConstituentDataItem_tbl] (
    [indexCompanyId]           INT              NOT NULL,
    [constituentId]            INT              NOT NULL,
    [pricingDate]              SMALLDATETIME    NULL,
    [dataItemId]               INT              NOT NULL,
    [dataItemValue]            NUMERIC (38, 16) NOT NULL,
    [constituentTradingItemId] INT              NULL
);


GO
CREATE CLUSTERED INDEX [IX_Russell2_Stg_PriceIndexConstituentDataItem_tbl]
    ON [dbo].[Russell2_Stg_PriceIndexConstituentDataItem_tbl]([dataItemId] ASC, [pricingDate] ASC, [constituentId] ASC);


GO
CREATE TABLE [dbo].[Russell2_Stg_PriceIndexConstituent_tbl] (
    [pricingDate]              SMALLDATETIME   NULL,
    [priceOpen]                NUMERIC (28, 6) NULL,
    [priceClose]               NUMERIC (28, 6) NULL,
    [bestPrice]                NUMERIC (28, 6) NOT NULL,
    [bestPriceDate]            SMALLDATETIME   NULL,
    [symbolValue]              VARCHAR (100)   NOT NULL,
    [sharesOutstanding]        BIGINT          NULL,
    [currencyId]               SMALLINT        NOT NULL,
    [exchangeRate]             NUMERIC (28, 6) NOT NULL,
    [usdPriceClose]            FLOAT (53)      NULL,
    [constituentId]            INT             NOT NULL,
    [constituentTradingItemId] INT             NULL
);


GO
CREATE UNIQUE CLUSTERED INDEX [IX_Russell2_Stg_PriceIndexConstituent_tbl]
    ON [dbo].[Russell2_Stg_PriceIndexConstituent_tbl]([constituentId] ASC, [pricingDate] ASC);


GO
CREATE TABLE [dbo].[Russell2_Stg_PriceIndexDataItem_tbl] (
    [tradingItemId] INT              NOT NULL,
    [pricingDate]   SMALLDATETIME    NOT NULL,
    [dataItemId]    INT              NOT NULL,
    [dataItemValue] NUMERIC (38, 16) NOT NULL,
    [currencyId]    INT              NULL,
    CONSTRAINT [PK_Russell2_Stg_PriceIndexDataItem_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [tradingItemId] ASC, [pricingDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_PriceIndexSecurityDataItem_tbl] (
    [constituentId]            INT              NOT NULL,
    [pricingDate]              SMALLDATETIME    NOT NULL,
    [dataItemId]               INT              NOT NULL,
    [dataItemValue]            NUMERIC (38, 16) NOT NULL,
    [constituentTradingItemId] INT              NULL,
    CONSTRAINT [PK_Russell2_Stg_PriceIndexSecurityDataItem_tbl] PRIMARY KEY CLUSTERED ([pricingDate] ASC, [constituentId] ASC, [dataItemId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_PriceIndex_tbl] (
    [tradingItemId]        INT              NOT NULL,
    [pricingDate]          SMALLDATETIME    NULL,
    [priceClose]           NUMERIC (38, 14) NULL,
    [bestPrice]            NUMERIC (38, 14) NULL,
    [bestPriceDate]        SMALLDATETIME    NULL,
    [volume]               BIGINT           NULL,
    [adjustmentFactor]     NUMERIC (19, 10) NULL,
    [symbolValue]          VARCHAR (100)    NOT NULL,
    [price52WeekHigh]      NUMERIC (38, 14) NULL,
    [price52WeekLow]       NUMERIC (38, 14) NULL,
    [dailyPriceVolume]     NUMERIC (38, 6)  NULL,
    [beginAccruedMktValue] NUMERIC (38, 14) NULL,
    [endMktValue]          NUMERIC (38, 14) NULL,
    [cashDiv]              NUMERIC (28, 5)  NULL,
    [numCnt]               SMALLINT         NULL,
    [divisor]              NUMERIC (38, 14) NULL
);


GO
CREATE CLUSTERED INDEX [IX_Russell2_Stg_PriceIndex_tbl]
    ON [dbo].[Russell2_Stg_PriceIndex_tbl]([tradingItemId] ASC, [pricingDate] ASC);


GO
CREATE TABLE [dbo].[Russell2_Stg_Security_IndexConstituentData_tbl] (
    [securityId]    INT             NULL,
    [dataItemId]    INT             NOT NULL,
    [dataVendorId]  INT             NOT NULL,
    [fromDate]      SMALLDATETIME   NOT NULL,
    [toDate]        SMALLDATETIME   NULL,
    [stringValue]   NVARCHAR (200)  NULL,
    [dateValue]     SMALLDATETIME   NULL,
    [numericValue]  NUMERIC (38, 6) NULL,
    [intValue]      INT             NULL,
    [booleanValue]  BIT             NULL,
    [constituentId] INT             NOT NULL,
    [tradingItemId] INT             NULL,
    CONSTRAINT [PK_Russell2_Stg_Security_IndexConstituentData_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC, [dataItemId] ASC, [fromDate] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_Security_IndexCorporateAction_tbl] (
    [effectiveDate]            DATE             NULL,
    [constituentID]            INT              NULL,
    [reason]                   VARCHAR (125)    NULL,
    [action]                   VARCHAR (15)     NULL,
    [indexFlags]               VARCHAR (29)     NOT NULL,
    [vFlag]                    INT              NOT NULL,
    [gFlag]                    INT              NOT NULL,
    [ICATypeId]                TINYINT          NULL,
    [capitalAdjustment]        NUMERIC (38, 12) NULL,
    [indexShareChange]         BIGINT           NULL,
    [indexSharesOutstanding]   BIGINT           NULL,
    [indexShareChange_V]       BIGINT           NULL,
    [indexSharesOutstanding_V] BIGINT           NULL,
    [indexShareChange_G]       BIGINT           NULL,
    [indexSharesOutstanding_G] BIGINT           NULL,
    [dividend]                 NUMERIC (38, 12) NULL,
    [new_CUSIP]                CHAR (9)         NULL,
    [old_CUSIP]                CHAR (9)         NULL,
    [new_companyName]          VARCHAR (255)    NULL,
    [old_companyName]          VARCHAR (255)    NULL,
    [new_isin]                 CHAR (12)        NULL,
    [old_isin]                 CHAR (12)        NULL,
    [new_ticker]               VARCHAR (25)     NULL,
    [old_ticker]               VARCHAR (25)     NULL,
    [new_exchange]             VARCHAR (10)     NULL,
    [old_exchange]             VARCHAR (10)     NULL,
    [dataVendorId]             INT              NOT NULL,
    [new_subs]                 CHAR (4)         NULL,
    [old_subs]                 CHAR (4)         NULL,
    [new_ES]                   CHAR (2)         NULL,
    [old_ES]                   CHAR (2)         NULL,
    [new_ind]                  CHAR (7)         NULL,
    [old_ind]                  CHAR (7)         NULL
);


GO
CREATE CLUSTERED INDEX [PK_Russell2_Stg_Security_IndexCorporateAction_tbl]
    ON [dbo].[Russell2_Stg_Security_IndexCorporateAction_tbl]([effectiveDate] ASC, [constituentID] ASC, [ICATypeId] ASC);


GO
CREATE TABLE [dbo].[Russell2_Stg_Security_tbl] (
    [securityId]           INT            NOT NULL,
    [securityName]         VARCHAR (100)  NOT NULL,
    [primaryFlag]          BIT            NOT NULL,
    [securityStartDate]    SMALLDATETIME  NULL,
    [securityEndDate]      SMALLDATETIME  NULL,
    [underlyingSedol]      VARCHAR (7)    NULL,
    [underlyingRatio]      NUMERIC (9, 4) NULL,
    [suggestedPrimaryflag] BIT            NOT NULL,
    [issuerCode]           VARCHAR (7)    NULL,
    [securitySubTypeId]    SMALLINT       NOT NULL,
    [isNAFlag]             BIT            NOT NULL,
    [isINTLFlag]           BIT            NOT NULL,
    [securityLevelId]      SMALLINT       NULL,
    [bondTypeId]           SMALLINT       NULL,
    [companyId]            INT            NULL,
    CONSTRAINT [PK_Russell2_Stg_Security_tbl] PRIMARY KEY CLUSTERED ([securityId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_SubType_tbl] (
    [subTypeId]        INT           NOT NULL,
    [subTypeValue]     VARCHAR (500) NULL,
    [childLevel]       SMALLINT      NULL,
    [sourceIdentifier] VARCHAR (30)  NULL,
    [charTypeId]       SMALLINT      NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_SubType_tbl] PRIMARY KEY CLUSTERED ([subTypeId] ASC)
);


GO
CREATE TABLE [dbo].[Russell2_Stg_TradingItem_tbl] (
    [tradingItemId]     INT     NOT NULL,
    [tradingItemTypeId] TINYINT NOT NULL,
    [currencyId]        INT     NULL,
    [securityId]        INT     NOT NULL,
    CONSTRAINT [PK_Russell2_Stg_TradingItem_tbl] PRIMARY KEY CLUSTERED ([tradingItemId] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_ConstituentDates_tbl] (
    [constituentId] INT           NOT NULL,
    [readingDate]   SMALLDATETIME NOT NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_ConstituentDates_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC, [readingDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_ConstituentIdentifier_tbl] (
    [constituentId]    INT            NOT NULL,
    [identifierTypeId] TINYINT        NOT NULL,
    [fromDate]         DATETIME       NOT NULL,
    [identifierValue]  NVARCHAR (300) NOT NULL,
    [toDate]           DATETIME       NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_ConstituentIdentifier_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC, [identifierTypeId] ASC, [fromDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_Constituent_tbl] (
    [constituentId] INT NOT NULL,
    [securityId]    INT NULL,
    [tradingItemId] INT NULL,
    [currencyId]    INT NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_Constituent_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexConstituentValue_Value112119_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] BIT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexConstituentValue_Value112119_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexConstituentValue_Value112120_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] BIT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexConstituentValue_Value112120_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexConstituentValue_Value112121WithSum_tbl] (
    [indexId]            INT              NOT NULL,
    [valueDate]          DATETIME         NOT NULL,
    [portfolioMarketCap] NUMERIC (38, 17) NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexConstituentValue_Value112121WithSum_tbl] PRIMARY KEY CLUSTERED ([indexId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexConstituentValue_Value112121_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] BIT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexConstituentValue_Value112121_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexConstituent_tbl] (
    [indexID]       INT      NOT NULL,
    [constituentID] INT      NOT NULL,
    [fromDate]      DATETIME NOT NULL,
    [toDate]        DATETIME NULL,
    [tradingItemId] INT      NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexConstituent_tbl] PRIMARY KEY CLUSTERED ([indexID] ASC, [constituentID] ASC, [fromDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexCorporateAction_tbl] (
    [indexID]       INT              NOT NULL,
    [constituentID] INT              NOT NULL,
    [seqID]         BIGINT           NOT NULL,
    [ICATypeId]     TINYINT          NOT NULL,
    [valueDate]     DATETIME         NOT NULL,
    [dataItemId]    INT              NOT NULL,
    [numericValue]  NUMERIC (38, 14) NULL,
    [textValue]     VARCHAR (200)    NULL,
    [tradingItemId] INT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexCorporateAction_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexID] ASC, [constituentID] ASC, [seqID] ASC, [ICATypeId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexRel_tbl] (
    [compositeIndexID] INT NOT NULL,
    [indexID]          INT NOT NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexRel_tbl] PRIMARY KEY CLUSTERED ([compositeIndexID] ASC, [indexID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value106368_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value106368_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value106369_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value106369_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value106370_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value106370_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value113152_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value113152_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value113153_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value113153_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value113154_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value113154_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value114893_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value114893_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value114894_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value114894_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value114895_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value114895_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value114896_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value114896_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value601835_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value601835_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value601836_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value601836_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value601837_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value601837_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value601838_tbl] (
    [indexProviderID] INT           NOT NULL,
    [constituentID]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemID]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemId]   INT           NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityTextCurrent_Value601838_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112032_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112032_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112033_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112033_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112034_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112034_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112109_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112109_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112110_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112110_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112111_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112111_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112112_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112112_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112113_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112113_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112114_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112114_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112115_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112115_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112117_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112117_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_Value112118_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_Value112118_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexSecurityValue_ValueOther_tbl] (
    [indexProviderID] INT             NOT NULL,
    [constituentID]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyID]      INT             NOT NULL,
    [dataItemID]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemId]   INT             NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexSecurityValue_ValueOther_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [indexProviderID] ASC, [constituentID] ASC, [valueDate] ASC, [currencyID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexToFeedType_tbl] (
    [feedTypeId]     SMALLINT      NOT NULL,
    [indexCompanyId] INT           NOT NULL,
    [inceptionDate]  SMALLDATETIME NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexToFeedType_tbl] PRIMARY KEY CLUSTERED ([indexCompanyId] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexTradingItem_tbl] (
    [IndexId]           INT     NOT NULL,
    [tradingItemId]     INT     NOT NULL,
    [tradingItemTypeId] TINYINT NOT NULL,
    [currencyId]        INT     NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexTradingItem_tbl] PRIMARY KEY CLUSTERED ([tradingItemId] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexValue_Value112099_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexValue_Value112099_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexValue_Value112100_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexValue_Value112100_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexValue_Value112102_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexValue_Value112102_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexValue_Value112103_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexValue_Value112103_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexValue_Value112106_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexValue_Value112106_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_IndexValue_ValueOther_tbl] (
    [tradingItemID]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_IndexValue_ValueOther_tbl] PRIMARY KEY CLUSTERED ([dataItemID] ASC, [tradingItemID] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_Index_tbl] (
    [indexID]         INT           NOT NULL,
    [indexProviderId] SMALLINT      NOT NULL,
    [indexName]       VARCHAR (255) NULL,
    [inceptionDate]   SMALLDATETIME NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_Index_tbl] PRIMARY KEY CLUSTERED ([indexID] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_PortfolioSnapshot_tbl] (
    [indexId]           INT              NOT NULL,
    [constituentId]     INT              NOT NULL,
    [fromDate]          SMALLDATETIME    NOT NULL,
    [toDate]            SMALLDATETIME    NOT NULL,
    [sharesOutstanding] DECIMAL (38, 16) NOT NULL,
    [tradingItemId]     INT              NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_PortfolioSnapshot_tbl] PRIMARY KEY CLUSTERED ([indexId] ASC, [constituentId] ASC, [fromDate] ASC, [toDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellMicrocap2_Stg_Portfolio_tbl] (
    [portfolioId] INT      NOT NULL,
    [objectId]    INT      NOT NULL,
    [currencyId]  SMALLINT NOT NULL,
    CONSTRAINT [PK_RussellMicrocap2_Stg_Portfolio_tbl] PRIMARY KEY CLUSTERED ([portfolioId] ASC, [objectId] ASC)
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_ConstituentDates_tbl] (
    [constituentId] INT           NULL,
    [readingDate]   SMALLDATETIME NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_ConstituentIdentifier_tbl] (
    [constituentId]    INT            NOT NULL,
    [identifierTypeId] TINYINT        NOT NULL,
    [fromDate]         DATETIME       NOT NULL,
    [identifierValue]  NVARCHAR (300) NOT NULL,
    [toDate]           DATETIME       NULL
);


GO
CREATE UNIQUE CLUSTERED INDEX [PK_RussellUS2_Stg_ConstituentIdentifier_tbl]
    ON [dbo].[RussellUS2_Stg_ConstituentIdentifier_tbl]([constituentId] ASC, [identifierTypeId] ASC, [fromDate] ASC);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_Constituent_tbl] (
    [constituentId] INT NOT NULL,
    [securityID]    INT NULL,
    [tradingItemID] INT NULL,
    [currencyID]    INT NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexConstituentValue_Value112119_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      SMALLDATETIME    NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] INT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_RussellUS2_Stg_IndexConstituentValue_Value112119_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexConstituentValue_Value112120_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      SMALLDATETIME    NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] INT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_RussellUS2_Stg_IndexConstituentValue_Value112120_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexConstituentValue_Value112121WithSum_tbl] (
    [indexId]            INT              NOT NULL,
    [valueDate]          SMALLDATETIME    NOT NULL,
    [portfolioMarketCap] NUMERIC (38, 17) NULL,
    CONSTRAINT [PK_RussellUS2_Stg_IndexConstituentValue_Value112121WithSum_tbl] PRIMARY KEY CLUSTERED ([indexId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexConstituentValue_Value112121_tbl] (
    [indexId]        INT              NOT NULL,
    [constituentId]  INT              NOT NULL,
    [valueDate]      SMALLDATETIME    NOT NULL,
    [dataItemId]     INT              NOT NULL,
    [value]          NUMERIC (38, 17) NULL,
    [endOfMonthFlag] INT              NULL,
    [tradingItemId]  INT              NULL,
    CONSTRAINT [PK_RussellUS2_Stg_IndexConstituentValue_Value112121_tbl] PRIMARY KEY CLUSTERED ([dataItemId] ASC, [indexId] ASC, [constituentId] ASC, [valueDate] ASC)
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexConstituent_tbl] (
    [indexId]       INT      NOT NULL,
    [constituentID] INT      NOT NULL,
    [fromDate]      DATETIME NOT NULL,
    [toDate]        DATETIME NULL,
    [tradingItemID] INT      NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexCorporateAction5Year_tbl] (
    [indexId]       INT              NOT NULL,
    [constituentId] INT              NOT NULL,
    [seqId]         BIGINT           NOT NULL,
    [ICATypeId]     TINYINT          NOT NULL,
    [valueDate]     DATETIME         NOT NULL,
    [dataItemId]    INT              NOT NULL,
    [numericValue]  NUMERIC (38, 14) NULL,
    [textValue]     VARCHAR (200)    NULL,
    [tradingItemID] INT              NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexCorporateAction_tbl] (
    [indexId]       INT              NOT NULL,
    [constituentId] INT              NOT NULL,
    [seqId]         BIGINT           NOT NULL,
    [ICATypeId]     TINYINT          NOT NULL,
    [valueDate]     DATETIME         NOT NULL,
    [dataItemId]    INT              NOT NULL,
    [numericValue]  NUMERIC (38, 14) NULL,
    [textValue]     VARCHAR (200)    NULL,
    [tradingItemID] INT              NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexRel_tbl] (
    [compositeIndexId] INT NOT NULL,
    [indexID]          INT NOT NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexSecurityTextCurrent5Year_tbl] (
    [indexProviderId] INT           NOT NULL,
    [constituentId]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemId]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemID]   INT           NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexSecurityTextCurrent_tbl] (
    [indexProviderId] INT           NOT NULL,
    [constituentId]   INT           NOT NULL,
    [valueDate]       SMALLDATETIME NOT NULL,
    [dataItemId]      INT           NOT NULL,
    [value]           VARCHAR (200) NULL,
    [endOfMonthFlag]  INT           NULL,
    [tradingItemID]   INT           NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexSecurityValue_tbl] (
    [indexProviderId] INT             NOT NULL,
    [constituentId]   INT             NOT NULL,
    [valueDate]       SMALLDATETIME   NOT NULL,
    [currencyId]      INT             NOT NULL,
    [dataItemId]      INT             NOT NULL,
    [value]           NUMERIC (38, 6) NULL,
    [endOfMonthFlag]  INT             NOT NULL,
    [tradingItemID]   INT             NULL
);


GO
CREATE UNIQUE CLUSTERED INDEX [PK_RussellUS2_Stg_IndexSecurityValue_tbl]
    ON [dbo].[RussellUS2_Stg_IndexSecurityValue_tbl]([indexProviderId] ASC, [constituentId] ASC, [valueDate] ASC, [currencyId] ASC, [dataItemId] ASC);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexToFeedType_tbl] (
    [feedTypeId]     SMALLINT      NOT NULL,
    [indexCompanyId] INT           NOT NULL,
    [inceptionDate]  SMALLDATETIME NULL,
    CONSTRAINT [PK_RussellUS2_Stg_IndexToFeedType_tbl] PRIMARY KEY CLUSTERED ([indexCompanyId] ASC)
);


GO
CREATE TABLE [dbo].[RussellUS2_stg_IndexTradingItem_tbl] (
    [indexId]           INT     NOT NULL,
    [tradingItemID]     INT     NOT NULL,
    [tradingItemTypeId] TINYINT NOT NULL,
    [currencyID]        INT     NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexValue5Year_tbl] (
    [tradingItemId]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_IndexValue_tbl] (
    [tradingItemId]  INT              NOT NULL,
    [valueDate]      DATETIME         NOT NULL,
    [dataItemID]     INT              NOT NULL,
    [value]          NUMERIC (38, 14) NULL,
    [endOfMonthFlag] BIT              NULL
);


GO
CREATE TABLE [dbo].[RussellUS2_stg_Index_tbl] (
    [indexId]         INT           NOT NULL,
    [indexProviderID] SMALLINT      NOT NULL,
    [indexName]       VARCHAR (255) NULL
);


GO
CREATE UNIQUE CLUSTERED INDEX [PK_RussellUS2_Stg_Index_tbl]
    ON [dbo].[RussellUS2_stg_Index_tbl]([indexId] ASC, [indexProviderID] ASC);


GO
CREATE TABLE [dbo].[RussellUS2_Stg_Portfolio_tbl] (
    [portfolioId] INT      NOT NULL,
    [objectId]    INT      NOT NULL,
    [currencyId]  SMALLINT NOT NULL,
    CONSTRAINT [PK_RussellUS2_Stg_Portfolio_tbl] PRIMARY KEY CLUSTERED ([portfolioId] ASC, [objectId] ASC)
);


GO
CREATE TABLE [dbo].[RussellV2_Stg_Constituent_tbl] (
    [constituentId]       INT NOT NULL,
    [securityId]          INT NULL,
    [tradingItemId]       INT NULL,
    [currencyId]          INT NULL,
    [cachedTradingItemId] INT NULL,
    CONSTRAINT [PK_RussellV2_Stg_Constituent_tbl] PRIMARY KEY CLUSTERED ([constituentId] ASC)
);


GO
